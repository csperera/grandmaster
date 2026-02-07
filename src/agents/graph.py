from typing import List, Union, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from src.agents.state import NavigatorState
from src.engine.calculator import compute_ev
from src.engine.models import StrategyNode, Outcome

def format_recommendations(node: StrategyNode) -> str:
    """Sorts children by weighted EV and generates a professional recommendation string."""
    # We want children that are fully defined
    children = [c for c in node.children if (isinstance(c, Outcome) or (isinstance(c, StrategyNode) and c.expected_value is not None))]
    
    def get_weighted_ev(child):
        if isinstance(child, Outcome):
            return child.probability * child.value
        return child.probability * child.expected_value

    def get_raw_value(child):
        if isinstance(child, Outcome):
            return child.value
        return child.expected_value

    sorted_children = sorted(
        children, 
        key=get_weighted_ev,
        reverse=True
    )
    
    if not sorted_children:
        return "No moves analyzed yet."
        
    recommendations = []
    top_n = min(len(sorted_children), 3)
    labels = ["optimal move", "second-best move", "third-best move"]
    
    for i in range(top_n):
        child = sorted_children[i]
        ev = get_weighted_ev(child)
        val = get_raw_value(child)
        prob = child.probability * 100
        recommendations.append(f"{labels[i]} is [{child.name}] with an EV of [{ev:.2f}] ([{val:.2f}] at [{prob:.0f}]%)")
        
    result = "The " + ", the ".join(recommendations) + "."
    return result

def prompt_user(state: NavigatorState):
    """Generates the next prompt based on the interview phase."""
    phase = state['interview_phase']
    msg = ""
    
    if phase == 'START':
        msg = "Welcome, Architect. What is the name of this strategy?"
    elif phase == 'GET_COUNT':
        msg = f"How many Outcomes are possible for '{state['active_parent_node'].name}'?"
    elif phase == 'COLLECT_OUTCOMES':
        idx = state['current_index'] + 1
        budget = (1.0 - state['running_prob_total']) * 100
        step = state['next_step']
        if step == 'AWAITING_NAME':
            msg = f"What is Outcome {idx} called?"
        elif step == 'AWAITING_PROB':
            msg = f"What is the probability (%) for '{state['pending_data']['name']}'? (Current budget remaining: {budget:.1f}%)"
        elif step == 'AWAITING_VALUE':
            msg = f"What is the financial value/payoff of '{state['pending_data']['name']}'? (Enter 0 if you plan to drill deeper later)"
    elif phase == 'DECIDE_NEXT_STEP':
        summary = format_recommendations(state['root_node'])
        msg = f"Current Rankings:\n{summary}\n\nWould you like to 'drill' deeper into one of these outcomes, or are we 'finished'?"

    return {
        **state,
        "recommendation_summary": msg
    }

def process_input(state: NavigatorState):
    """Handles Guided Interview logic and state transitions."""
    user_input = state.get('latest_input')
    if user_input is None:
        return state

    phase = state['interview_phase']
    
    if phase == 'START':
        strategy_name = user_input.strip()
        root = StrategyNode(name=strategy_name, node_type="decision")
        return {
            **state,
            "root_node": root,
            "active_parent_node": root,
            "interview_phase": 'GET_COUNT',
            "latest_input": None
        }

    if phase == 'GET_COUNT':
        try:
            count = int(user_input.strip())
            return {
                **state,
                "target_count": count,
                "current_index": 0,
                "running_prob_total": 0.0,
                "interview_phase": 'COLLECT_OUTCOMES',
                "next_step": 'AWAITING_NAME',
                "latest_input": None
            }
        except ValueError:
            return state

    if phase == 'COLLECT_OUTCOMES':
        step = state['next_step']
        new_pending = {**state['pending_data']}
        
        if step == 'AWAITING_NAME':
            new_pending['name'] = user_input.strip()
            return {**state, "pending_data": new_pending, "next_step": 'AWAITING_PROB', "latest_input": None}
            
        if step == 'AWAITING_PROB':
            try:
                raw_val = user_input.strip().replace('%', '')
                prob = float(raw_val) / 100.0
                new_pending['probability'] = prob
                return {**state, "pending_data": new_pending, "next_step": 'AWAITING_VALUE', "latest_input": None}
            except ValueError:
                return state

        if step == 'AWAITING_VALUE':
            try:
                val = float(user_input.strip())
                new_pending['value'] = val
                return {**state, "pending_data": new_pending, "next_step": 'COMMIT', "latest_input": None}
            except ValueError:
                return state

    if phase == 'DECIDE_NEXT_STEP':
        if user_input.lower() == 'finished':
            return {**state, "interview_phase": 'COMPLETE', "latest_input": None}
        else:
            found_node = None
            for child in state['active_parent_node'].children:
                if child.name == user_input:
                    found_node = child
                    break
            
            if found_node and isinstance(found_node, StrategyNode):
                return {
                    **state,
                    "active_parent_node": found_node,
                    "interview_phase": 'GET_COUNT',
                    "latest_input": None
                }
            elif found_node and isinstance(found_node, Outcome):
                new_node = StrategyNode(
                    name=found_node.name,
                    probability=found_node.probability,
                    node_type="chance"
                )
                idx = state['active_parent_node'].children.index(found_node)
                state['active_parent_node'].children[idx] = new_node
                
                return {
                    **state,
                    "active_parent_node": new_node,
                    "interview_phase": 'GET_COUNT',
                    "latest_input": None
                }

    return state

def update_tree(state: NavigatorState):
    """Commits outcomes and handles batch validation."""
    if state['interview_phase'] != 'COLLECT_OUTCOMES' or state['next_step'] != 'COMMIT':
        return state
        
    new_pending = state['pending_data']
    
    new_child = Outcome(
        name=new_pending['name'],
        probability=new_pending['probability'],
        value=new_pending['value']
    )
    
    new_total = state['running_prob_total'] + new_child.probability
    is_last = (state['current_index'] + 1 == state['target_count'])
    
    if is_last:
        if abs(new_total - 1.0) > 0.0001:
            diff = 1.0 - state['running_prob_total']
            new_child.probability = diff
            new_total = 1.0

    state['active_parent_node'].children.append(new_child)
    compute_ev(state['root_node'])
    
    if is_last:
        return {
            **state,
            "running_prob_total": new_total,
            "interview_phase": 'DECIDE_NEXT_STEP',
            "pending_data": {},
            "next_step": 'AWAITING_INPUT'
        }
    else:
        return {
            **state,
            "current_index": state['current_index'] + 1,
            "running_prob_total": new_total,
            "pending_data": {},
            "next_step": 'AWAITING_NAME'
        }

workflow = StateGraph(NavigatorState)
workflow.add_node("prompt_user", prompt_user)
workflow.add_node("process_input", process_input)
workflow.add_node("update_tree", update_tree)
workflow.set_entry_point("process_input")
workflow.add_edge("process_input", "update_tree")
workflow.add_edge("update_tree", "prompt_user")
workflow.add_edge("prompt_user", END)
graph = workflow.compile()

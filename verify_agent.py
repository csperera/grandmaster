from src.engine.models import StrategyNode, Outcome
from src.agents.state import NavigatorState
from src.agents.graph import graph, format_recommendations, process_input, update_tree

def test_recommendation_formatting():
    print("Testing recommendation formatting...")
    root = StrategyNode(name="Root", node_type="chance")
    root.children = [
        Outcome(name="Path A", probability=0.4, value=20.0),
        Outcome(name="Path B", probability=0.3, value=30.0),
        Outcome(name="Path C", probability=0.3, value=10.0),
    ]
    # No need to call compute_ev since they are Outcomes (base case)
    result = format_recommendations(root)
    print(f"Result: {result}")
    expected = "The optimal move is [Path B] with an EV of [30.00], the second-best move is [Path A] with an EV of [20.00], the third-best move is [Path C] with an EV of [10.00]."
    assert result == expected
    print("Recommendation formatting test passed!")

def test_graph_transitions():
    print("\nTesting graph transition logic...")
    root = StrategyNode(name="Main", node_type="chance")
    state: NavigatorState = {
        "messages": [],
        "root_node": root,
        "current_node_path": ["Main"],
        "pending_data": {},
        "next_step": "AWAITING_NAME",
        "latest_input": "New Node"
    }
    
    # 1. Process Name
    print("Step 1: Process Name")
    state = process_input(state)
    print(f"Pending data: {state['pending_data']}")
    assert state['pending_data']['name'] == "New Node"
    assert state['next_step'] == "AWAITING_PROB"
    
    # 2. Process Prob
    print("Step 2: Process Probability")
    state['latest_input'] = "0.5"
    state = process_input(state)
    assert state['pending_data']['probability'] == 0.5
    assert state['next_step'] == "COMMIT"
    
    # 3. Update Tree
    print("Step 3: Update Tree")
    state = update_tree(state)
    assert len(root.children) == 1
    assert root.children[0].name == "New Node"
    assert root.children[0].probability == 0.5
    assert state['next_step'] == "AWAITING_NAME"
    assert state['pending_data'] == {}
    
    print("Graph transitions test passed!")

if __name__ == "__main__":
    test_recommendation_formatting()
    test_graph_transitions()
    print("\nAll verification tests passed!")

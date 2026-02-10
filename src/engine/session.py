from src.engine.input_handler import get_outcomes_sequentially
from src.engine.models import StrategyNode, Outcome
from src.engine.calculator import compute_ev

def render_ascii_tree(node: StrategyNode):
    """Generates the ASCII visualization with calculated EV per branch."""
    lines = []
    lines.append(f"\nScenario: {node.name}")
    
    if not node.children:
        return "No outcomes to display."

    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        connector = "└── " if is_last else "├── "
        
        # Calculate the specific EV contribution for this branch
        # (Probability * Payoff)
        branch_ev = child.probability * (child.value if isinstance(child, Outcome) else child.expected_value)
        
        # Format the display for clarity
        prob_display = f"P={child.probability:.2f}"
        val = child.value if isinstance(child, Outcome) else child.expected_value
        
        lines.append(f"  {connector}({prob_display}, Payoff={val}) -> {child.name} | EV: {branch_ev:.1f}")

    return "\n".join(lines)

def run_v01_session():
    print("\n" + "="*40)
    print("      GRANDMASTER V0.1: ACTIVE")
    print("="*40)
    
    scenario_name = input("What is this scenario called? ")
    try:
        num_outcomes = int(input("How many outcomes are possible? "))
    except ValueError:
        print("Error: Please enter a whole number.")
        return

    # 1. Collect Outcomes via sequential input flow
    outcomes = get_outcomes_sequentially(num_outcomes)
    
    # 2. Initialize the model
    root_node = StrategyNode(
        name=scenario_name,
        node_type="chance",
        children=outcomes
    )
    
    # 3. Process calculations
    compute_ev(root_node)
    
    # 4. Identify the highest EV contributor for the recommendation
    best_outcome = max(root_node.children, key=lambda c: c.probability * c.value)
    best_contribution = best_outcome.probability * best_outcome.value

    # 5. Output Visuals
    print("\n--- VISUAL MODEL ---")
    print(render_ascii_tree(root_node))
    
    # 6. Final Strategic Recommendation (Total EV removed per request)
    print("\n" + "-"*60)
    print(f"STRATEGIC RECOMMENDATION: {best_outcome.name.upper()} WITH EV OF {best_contribution:.1f}")
    print("-" * 60 + "\n")
    
    return root_node
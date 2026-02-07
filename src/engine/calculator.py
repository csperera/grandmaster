from src.engine.models import StrategyNode, Outcome

def compute_ev(node: StrategyNode | Outcome) -> float:
    """Recursively calculates weighted Expected Value."""
    # Base Case: It's a final outcome
    if isinstance(node, Outcome):
        return node.value

    if not node.children:
        return 0.0

    # Calculate EV of all children recursively
    child_evs = [compute_ev(child) for child in node.children]

    if node.node_type == "decision":
        # Strategy: Pick the best possible branch
        node.expected_value = max(child_evs)
    else:
        # Strategy: Weighted sum based on probabilities
        total_ev = 0.0
        for child in node.children:
            # We use the probability of the child (Outcome or nested StrategyNode)
            total_ev += child.probability * compute_ev(child)
        node.expected_value = total_ev
        
    return node.expected_value
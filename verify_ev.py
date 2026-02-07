from src.engine.models import StrategyNode, Outcome
from src.agents.graph import format_recommendations
from src.engine.calculator import compute_ev

def test_refined_recommendations():
    print("Testing refined recommendation formatting...")
    # Bond Strategy Example
    # Aggressive Long Bonds: 60% of 2000 -> EV 1200
    # Short Term Cash: 40% of 500 -> EV 200
    root = StrategyNode(name="Bond Strategy", node_type="chance")
    root.children = [
        Outcome(name="Aggressive Long Bonds", probability=0.6, value=2000.0),
        Outcome(name="Short Term Cash", probability=0.4, value=500.0),
    ]
    
    # Compute EV for the tree (sets root.expected_value)
    compute_ev(root)
    
    result = format_recommendations(root)
    print(f"Result:\n{result}")
    
    expected = "The optimal move is [Aggressive Long Bonds] with an EV of [1200.00] ([2000.00] at [60]%), the second-best move is [Short Term Cash] with an EV of [200.00] ([500.00] at [40]%)."
    assert result == expected
    print("Refined recommendation formatting test passed!")

if __name__ == "__main__":
    test_refined_recommendations()

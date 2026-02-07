import pytest
from src.engine.models import StrategyNode, Outcome
from src.engine.calculator import compute_ev

def test_weighted_ev_calculation():
    """Test a simple chance node (TLT Example)."""
    # Expected: (0.4 * 22) + (0.35 * 5) + (0.25 * -12) = 7.55
    outcomes = [
        Outcome(name="Up", probability=0.4, value=22.0),
        Outcome(name="Same", probability=0.35, value=5.0),
        Outcome(name="Down", probability=0.25, value=-12.0)
    ]
    root = StrategyNode(name="TLT Choice", node_type="chance", children=outcomes)
    assert compute_ev(root) == pytest.approx(7.55)

def test_nested_decision_strategy():
    """Napoleon's Test: Choosing between a safe path and a risky but high-EV path."""
    # Path 1: Safe (100% chance of 10)
    safe_path = StrategyNode(
        name="Safe Path", 
        node_type="chance", 
        probability=0.5, # This is the probability of this branch existing
        children=[Outcome(name="Guaranteed", probability=1.0, value=10.0)]
    )
    
    # Path 2: Risky (100% chance of 20)
    risky_path = StrategyNode(
        name="Risky Path", 
        node_type="chance", 
        probability=0.5, 
        children=[Outcome(name="High Reward", probability=1.0, value=20.0)]
    )
    
    root = StrategyNode(
        name="Root Decision", 
        node_type="decision", 
        children=[safe_path, risky_path]
    )
    
    # Decision node picks the max of child EVs (10 vs 20)
    assert compute_ev(root) == 20.0
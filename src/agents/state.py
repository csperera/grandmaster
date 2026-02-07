from typing import TypedDict, List, Annotated, Dict, Any, Optional, Union
import operator
from src.engine.models import StrategyNode, Outcome

class NavigatorState(TypedDict):
    """
    State for the GrandMaster Strategy Navigator.
    
    Attributes:
        messages: Append-only list of strings for conversation history.
        root_node: The full StrategyNode tree.
        current_node_path: List of IDs/names to track where the user is in the tree.
        pending_data: Dictionary to store name, type, and probability while mid-process.
        next_step: State machine indicator (e.g., 'AWAITING_NAME', 'AWAITING_PROB').
        latest_input: The most recent input received from the user.
        recommendation_summary: Formatted string of current top moves.
        interview_phase: Current phase of the guided interview ('START', 'GET_COUNT', 'COLLECT_OUTCOMES', 'DECIDE_NEXT_STEP').
        target_count: The number of outcomes desired for the current node.
        current_index: Index of the outcome being defined.
        running_prob_total: Sum of probabilities entered so far (0.0 to 1.0).
        active_parent_node: Reference to the node being built (StrategyNode).
    """
    messages: Annotated[List[str], operator.add]
    root_node: StrategyNode
    current_node_path: List[str]
    pending_data: Dict[str, Any]
    next_step: str
    latest_input: Optional[str]
    recommendation_summary: str
    interview_phase: str
    target_count: int
    current_index: int
    running_prob_total: float
    active_parent_node: StrategyNode
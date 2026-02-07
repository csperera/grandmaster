import sys
from src.engine.models import StrategyNode
from src.agents.state import NavigatorState
from src.agents.graph import graph

def main():
    print("--- GrandMaster: Guided Strategy Interview ---")
    print("Architectural Directive: Strategic Navigator Active.")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    state: NavigatorState = {
        "messages": [],
        "root_node": None,
        "current_node_path": [],
        "pending_data": {},
        "next_step": "AWAITING_NAME",
        "latest_input": None,
        "recommendation_summary": "",
        "interview_phase": 'START',
        "target_count": 0,
        "current_index": 0,
        "running_prob_total": 0.0,
        "active_parent_node": None
    }
    
    while True:
        state = graph.invoke(state)
        
        if state['interview_phase'] == 'COMPLETE':
            print("\nInterview Complete. Strategic model finalized.")
            break
            
        print(f"\n{state['recommendation_summary']}")
        
        try:
            user_input = input(">> ").strip()
        except EOFError:
            break
        
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting GrandMaster.")
            break
            
        state["latest_input"] = user_input

if __name__ == "__main__":
    main()

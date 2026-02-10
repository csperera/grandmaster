import os
from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from dotenv import load_dotenv, find_dotenv # Imported find_dotenv

from src.engine.input_handler import get_outcomes_sequentially
from src.engine.models import StrategyNode, Outcome
from src.engine.calculator import compute_ev

def get_client():
    """
    Hunts for the .env file in the directory tree and forces a reload.
    """
    # 1. This finds the .env file even if you are in a subfolder
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path) 
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    # DEBUG: Help confirm if the key is actually loading
    if not api_key:
        print(f"❌ DEBUG: find_dotenv() found: '{dotenv_path}'")
        print("❌ DEBUG: OPENAI_API_KEY is still missing from that file!")
    else:
        print(f"✅ DEBUG: Success! Loaded from {dotenv_path}")

    # We pass the api_key explicitly to the client for robustness
    return wrap_openai(OpenAI(api_key=api_key))

def render_ascii_tree(node: StrategyNode):
    """Generates the ASCII visualization with calculated EV per branch."""
    lines = []
    lines.append(f"\nScenario: {node.name}")
    
    if not node.children:
        return "No outcomes to display."

    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        connector = "└── " if is_last else "├── "
        
        # Pull value based on whether it's a leaf node or branch
        val = child.value if isinstance(child, Outcome) else getattr(child, 'expected_value', 0)
        branch_ev = child.probability * val
        prob_display = f"P={child.probability:.2f}"
        
        lines.append(f"  {connector}({prob_display}, Payoff={val}) -> {child.name} | EV: {branch_ev:.1f}")

    return "\n".join(lines)

@traceable(name="Narrative Generator")
def get_ai_narrative(scenario, best_outcome, ev):
    """Calls GPT-4o-mini to explain the mathematical result in strategic terms."""
    try:
        client = get_client() # Client is created only when needed
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are the GrandMaster, a cold, calculating military strategist. Explain why a move is mathematically superior based on Expected Value."
                },
                {
                    "role": "user", 
                    "content": f"In the scenario '{scenario}', the most viable path is '{best_outcome}' with an EV of {ev}. Provide a brief, 2-sentence strategic justification."
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AI Analysis Unavailable: {e}]"

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
    
    # 4. Identify the best outcome
    best_outcome = max(root_node.children, key=lambda c: c.probability * (c.value if isinstance(c, Outcome) else c.expected_value))
    best_contribution = best_outcome.probability * (best_outcome.value if isinstance(best_outcome, Outcome) else best_outcome.expected_value)

    # 5. Output Visuals
    print("\n--- VISUAL MODEL ---")
    print(render_ascii_tree(root_node))
    
    # 6. GET AI NARRATIVE (The LangSmith "Demo" moment)
    print("\nConsulting GrandMaster for strategic insight...")
    analysis = get_ai_narrative(scenario_name, best_outcome.name, best_contribution)
    
    # 7. Final Strategic Recommendation
    print("\n" + "-"*60)
    print(f"STRATEGIC RECOMMENDATION: {best_outcome.name.upper()}")
    print(f"ANALYSIS: {analysis}")
    print("-" * 60 + "\n")
    
    return root_node
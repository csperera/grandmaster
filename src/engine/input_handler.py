from src.engine.models import Outcome

def get_outcomes_sequentially(num_outcomes: int):
    outcomes = []
    total_prob_percent = 0.0

    for i in range(1, num_outcomes + 1):
        print(f"\n--- Outcome {i} ---")
        name = input(f"What is Outcome {i} called? ")
        payoff = float(input(f"What is the numerical payoff for outcome '{name}'? "))
        
        # Logic for the final outcome's probability
        if i == num_outcomes:
            prob_percent = 100.0 - total_prob_percent
            print(f"Automatic assignment: Remaining {prob_percent}% assigned to '{name}'.")
        else:
            prob_percent = float(input(f"What is the probability percentage for outcome '{name}'? "))
            total_prob_percent += prob_percent

        # We convert to decimal here to satisfy the pydantic ge=0, le=1.0 constraint
        outcomes.append(Outcome(
            name=name, 
            value=payoff, 
            probability=prob_percent / 100.0
        ))
    
    return outcomes
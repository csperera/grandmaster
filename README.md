# GrandMaster

**GrandMaster** is a Quantitative Risk Management (QRM) and Decision Support System (DSS) designed to model complex scenarios through probabilistic tree analysis. It allows users to map out potential outcomes, assign financial or numerical payoffs, and determine the optimal path using Expected Value (EV) optimization.



## 🛠 Strategic Framework (QRM)

GrandMaster leverages **stochastic modeling** to transform qualitative "what-if" scenarios into quantitative data. By utilizing a tree structure, the software helps mitigate cognitive biases in risk assessment by forcing a disciplined look at:

* **Mutual Exclusivity:** Ensuring all possible outcomes are identified.
* **Probability Weighting:** Moving beyond "best-case/worst-case" thinking to a weighted average of reality.
* **EV Maximization:** Identifying the branch that provides the highest mathematical value over the long run.

---

## 🚀 Version 0.1: Stochastic "Chance" Modeling

The current version focuses on **Chance Nodes**—scenarios where the outcome is determined by external factors (market shifts, weather, or competitive actions).

### **Key Features**
* **Sequential Input Flow:** A guided CLI experience that collects Outcome Names, Payoffs, and Probabilities.
* **Auto-Balancing Probabilities:** The system automatically calculates the remainder for the final outcome to ensure a valid 100% probability distribution.
* **ASCII Model Visualization:** Renders a visual "Game Tree" directly in the terminal, displaying the EV contribution of every individual branch.
* **Strategic Recommendation:** Automatically highlights the primary driver of the scenario's value.



---

## 📈 Roadmap: Towards Version 1.0

The next evolution of GrandMaster moves from "What might happen" to "What should I do?" by introducing **Decision Nodes**.

### **Planned Features:**
* **Decision Nodes ($\square$):** Interleaved with Chance Nodes ($\bigcirc$) to model sequential choices.
* **Backward Induction:** The engine will "solve" the tree from right to left, pruning sub-optimal decision branches.
* **Sensitivity Analysis:** Identifying which probability or payoff changes have the greatest impact on the final decision.
* **JSON Exports:** Saving scenario models for historical audit trails and side-by-side comparisons.

---

## 🖥️ Getting Started

### **Installation**
1. Clone the repository:
   ```bash
   git clone [https://github.com/csperera/grandmaster.git](https://github.com/csperera/grandmaster.git)
   cd grandmaster


---
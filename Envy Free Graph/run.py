from fair_division_solver import FairDivisionSolver
import data

if __name__ == "__main__":
    
    solver = FairDivisionSolver(data.NUM_AGENTS, data.NUM_ITEMS, data.VALUATIONS)
    
    # allocation = data.INITIAL_ALLOCATION
    # --- Analyze any allocation to determin if EF1 ---
    # print("=== Allocation Analysis ===")
    # analysis = solver.analyze_allocation(allocation)
    # print(f"Allocation: {analysis['allocation']}")
    # print(f"Is Envy-Free: {analysis['is_envy_free']}")
    # print(f"Is EF1: {analysis['is_EF1']}")
    # print(f"Bundle Values (i vs j): {analysis['bundle_values_per_agent']}")
    # print(f"Envy Statistics: {analysis['envy_statistics']}")
    # solver.envy_graph.visualize("Initial Chores Allocation")
    
    # --- Run the EF1 algorithm on Agents and Goods ---
    print("\n=== Greedy EF1 Algorithm ===")
    ef1_allocation = solver.find_EF1_allocation()
    
    # Analyze the resulting allocation
    ef1_analysis = solver.analyze_allocation(ef1_allocation)
    print(f"EF1 Allocation: {ef1_analysis['allocation']}")
    print(f"Is Envy-Free: {ef1_analysis['is_envy_free']}")
    print(f"Is EF1: {ef1_analysis['is_EF1']}")
    print(f"Bundle Values[[agent 1 bundle, agent 2 bundle, etc.]]: {ef1_analysis['bundle_values_per_agent']}")
    print(f"Envy Statistics: {ef1_analysis['envy_statistics']}")

    solver.envy_graph.visualize("Greedy EF1 Result")
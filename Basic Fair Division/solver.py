import data
from fair_division_solver import FairDivisionSolver
import math

if __name__ == "__main__":
    solver = FairDivisionSolver(items = data.items, agents = data.agents, valuations = data.valuations)

    print("Generating Envy Free allocations for Divorce Settlement: ")
    envy_free_allocations, proportional_allocations = solver.generate_and_evaluate()
    total_allocations = 2**len(data.items)
    percentage_EV = (len(envy_free_allocations) / total_allocations) * 100
    percentage_P = (len(proportional_allocations) / total_allocations) * 100

    print("------------------------------------")
    print("Total number of allocations:" + str(total_allocations))
    print("The number of Envy-Free allocations: " + str(len(envy_free_allocations)))
    print("Perctange: "  + str(math.ceil(percentage_EV)) + "%") 
    # print("5 Envy-Free allocations")
    # for i in range(6):
    #     print(envy_free_allocations[i])

    print("------------------------------------")
    print("Total number of allocations:" + str(total_allocations))
    print("The number of Proportional allocations: " + str(len(proportional_allocations)))
    print("Perctange: "  + str(math.ceil(percentage_P)) + "%") 
    # print("5 Proportional Allocations: ")
    # for i in range(6):
    #     print(proportional_allocations[i])
    print("------------------------------------")


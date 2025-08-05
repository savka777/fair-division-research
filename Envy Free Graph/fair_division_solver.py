import data
from envy_graph import EnvyGraph
from typing import List, Dict

class FairDivisionSolver:

    def __init__(self, num_agents, num_items, valuations):
        self.num_agents = num_agents
        self.num_items = num_items
        self.valuations = valuations
        self.envy_graph = EnvyGraph(num_agents)
        
    def find_EF1_allocation(self) -> List[List[int]]:

        allocations = [[] for _ in range(self.num_agents)]

        # Process each item
        for item in range(self.num_items):
            self.envy_graph.build_envy_graph(allocations, self.valuations)

            sources = self.envy_graph.get_sources()
            if sources: 
                chose_agent = sources[0] # Chooses first source if multiple exist
            else:
                chose_agent = 0 # Fallback: should not happen in this algorithm

            allocations[chose_agent].append(item)

            allocations = self.envy_graph.eliminate_cycles(allocations)

        return allocations
    
    def get_bundle_values_per_agent(self, allocations, valuations) -> List[List[float]]:
        """
        Returns the value of each bundle as seen by every other agent.
        """
        all_values = []
        for i in range(self.num_agents):
            agent_values = []
            for j in range(self.num_agents):
                value = self.envy_graph.get_bundle_value(i, allocations[j], valuations)
                agent_values.append(value)
            all_values.append(agent_values)
        return all_values

    def analyze_allocation(self, allocation: List[List[int]]) -> Dict:
        """
        Provides a detailed analysis of a given allocation.
        """
        self.envy_graph.build_envy_graph(allocation, self.valuations)
        
        return {
            'allocation': allocation,
            'is_envy_free': self.envy_graph.is_envy_free(),
            'is_EF1': self.envy_graph.is_envy_free_1(allocation, self.valuations),
            'bundle_values_per_agent': self.get_bundle_values_per_agent(allocation, self.valuations),
            'envy_statistics': self.envy_graph.get_envy_statistics()
        }
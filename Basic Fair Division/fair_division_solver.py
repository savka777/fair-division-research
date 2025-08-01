from itertools import combinations

class FairDivisionSolver:
    
    def __init__(self, items, agents, valuations):
        self.items = items
        self.agents = agents
        self.valuations = valuations

    def generate_and_evaluate(self):
        """
        Calculates all possible allocations for two agents and
        determines which are envy-free and proportional.
        """
        EV_allocations = []
        P_allocations = []

        # Iterate through all possible subsets of items for agent 1
        for size in range(len(self.items) + 1):
            for agent_one_items in combinations(self.items, size):
                agent_one_list = list(agent_one_items)
                agent_two_list = []
            
                for item in self.items:
                    if item not in agent_one_list:
                        agent_two_list.append(item)
                
                allocation = {
                    self.agents[0]: agent_one_list,
                    self.agents[1]: agent_two_list
                }
                
                # Check for envy free and proportional properties
                if self.is_Envy_Free(allocation):
                    EV_allocations.append(allocation)
                
                if self.is_Proportional(allocation):
                    P_allocations.append(allocation)
        
        return EV_allocations, P_allocations

    def is_Envy_Free(self, allocation):
        """
        Checks if an allocation is envy-free.
        An allocation is envy-free if no agent prefers another agent's bundle to their own.
        """
       
        for agent in self.agents:
            agent_bundle = allocation[agent]
            
            for other_agent in self.agents:
                if agent != other_agent:
                    other_bundle = allocation[other_agent]
                    
                    my_bundle_value = self.calculate_bundle_value(agent, agent_bundle)
                    other_bundle_value = self.calculate_bundle_value(agent, other_bundle)
                    
                    if my_bundle_value < other_bundle_value:
                        return False  # Envy found
                        
        return True # No envy found for any agent
    
    def is_Proportional(self, allocation):
        """
        Checks if an allocation is proportional.
        An allocation is proportional if each agent's bundle is worth at least 1/n of the total value
        of all goods from their own perspective.
        """
        total_number_of_agents = len(self.agents)
        
        for agent in self.agents:
            agent_bundle = allocation[agent]
            
            # Calculate the value of the agent's bundle
            bundle_value = self.calculate_bundle_value(agent, agent_bundle)
            
            # Calculate the total value of all items from the agent's perspective
            total_value_of_all_goods = self.calculate_total_valuations(agent)
            
            proportional_share = total_value_of_all_goods / total_number_of_agents
            
            if bundle_value < proportional_share:
                return False  # Not proportional, an agent got less than their fair share
                
        return True  # All agents got their proportional share
        
    def calculate_bundle_value(self, agent, bundle):
        """
        Calculates the total value of a given bundle of goods from an agent's perspective.
        """
        total_value = 0
        agent_valuations = self.valuations[agent]

        for item in bundle:
            total_value += agent_valuations.get(item, 0)

        return total_value
    
    def calculate_total_valuations(self, agent):
        """
        Calculates the total value of all items from a single agent's perspective.
        """
        return sum(self.valuations[agent].values())
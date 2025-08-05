import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Set
import numpy as np

class EnvyGraph:
    """
    Liptons, Envy Free Graph, built for EF1. 
    """

    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(num_agents))
    
    def build_envy_graph(self, allocations, valuations): # allocation[i] = bundle for agent i. valuation[i][j] = value of item j to agent i
        """
        Build an Envy Graph of [n] nodes, and (i,j) edges of envy.

        Takes the current agent allocations (Thier bundles) and each agents valuation of all items, 
        and constructs and envy graph, if agent i envies agent j.
        """
        self.graph.clear_edges() 

        # build graph of [n] agents
        for i in range(self.num_agents):
            my_bundle_value = self.get_bundle_value(i, allocations[i], valuations)

            for j in range(self.num_agents):
                if i != j: 
                    their_bundle_value = self.get_bundle_value(i, allocations[j], valuations) # from presepective of i, valueing j's bundle

                    # if i envies j
                    if their_bundle_value > my_bundle_value: 
                        self.graph.add_edge(i, j, envy_amount = their_bundle_value - my_bundle_value) # add edge between agents (i,j) to indicate envy
                    
    def get_bundle_value(self, agent, bundle, valuations):
        """
        Returns the value of a bundle from the perspective of the current agent. 

        This is used to evaluate any bundle, from the perspective of the current agent
        """
        total_value = 0
        for item in bundle:
            total_value += valuations[agent][item] # Add to total_value the value the current agent places on the item in question
        
        return total_value
    
    def is_envy_free(self): # if no edges, than no envy
        """
        Checks if the graph has any envy. 

        A graph is envy free if there are no edges connected to any nodes. 
        """
        return len(self.graph.edges()) == 0
    
    def is_envy_free_1(self, allocations, valuations):
        """
        Check if the current graph is envy free up to 1 good
        """
        for i, j in self.graph.edges(): # iterate through all envy pairs
            if not self.check_EF1_condition(i, j, allocations, valuations): # check EF1 condition
                return False
        return True
    
    def check_EF1_condition(self, agent1, agent2, allocations, valuations):
        """
        Checks the EF1 condition between any two agents. 
        """
        if not allocations[agent2]: # if agent2's bundle is empty, no envy for agent1 
            return True

        my_bundle_value = self.get_bundle_value(agent1, allocations[agent1], valuations) # current agents bundle value

        # find max value in agent2's bundle according to agent 1's valuation
        max_value_in_agent2_bundle = -np.inf # empty, or absurd value for comparison
        for item in allocations[agent2]:
            max_value_in_agent2_bundle = max(max_value_in_agent2_bundle, valuations[agent1][item])
        
        # check EF1, if removing the best item from agent2's bundle removes envy
        agent2_value = self.get_bundle_value(agent1, allocations[agent2], valuations)
        agent2_value_minus_the_best = agent2_value - max_value_in_agent2_bundle

        if my_bundle_value >= agent2_value_minus_the_best:
            return True
        return False

    def get_sources(self): 
        """
        Returns a list of agents that no one envies. 

        An agent that no one envies has no in degrees.
        """
        sources = []
        for node in self.graph.nodes():
            if self.graph.in_degree(node) == 0:
                sources.append(node)
        
        return sources
    
    def get_sinks(self): 
        """
        Returns a list of agents that envy no one. 

        An agent that envies no one has no out degrees.
        """
        sinks = []
        for node in self.graph.nodes():
            if self.graph.out_degree(node) == 0:
                sinks.append(node)
        
        return sinks

    def has_cycles(self):
        """
        Check if current graph has cycles. 

        Uses topological sort, if a graph can be topologically sorted than its acyclic. 
        Otherwise, it contains a cycle.
        """
        try:
            nx.topological_sort(self.graph) # if top sort works than graph is acyclic
            return False
        except nx.NetworkXError:
            return True
    
    def get_cycles(self):
        """
        Returns a list of lists, that contain cycle combinations. 

        For example, [[0,1,2]] has one entry, with one cycle, where,
        agent 0 envies agent 1, 
        agent 1 envies agent 2,
        agent 2 envies agent 0,
        """
        try:
            return list(nx.simple_cycles(self.graph))
        except nx.NetworkXError:
            return [] 
    
    def eliminate_cycles(self, allocations): # allocations = [[item A, item B], [Item C], Items D]] where allocations[i] is a bundle for agent i 
        """
        Creating a copy of the allocation to work on.

        Identifying the envy cycles.

        For each cycle, collecting the bundles of the agents involved.

        Performing the rotation (by getting the next agent's bundle).
        """
        rotated_allocations = [bundle.copy() for bundle in allocations]
        
        cycles = self.get_cycles() # [0,1,2] = agent 0 envies agent 1, agent 1 envies agent 2, agent 2 envies agent 0 -> cycle!

        for cycle in cycles: # iterate through each cycle, which is a list of agents or nodes that create a cycle
            agent_cycle_bundles = [] # The bundles of each agent that is in the cycle list, so bundles for agent 0 = [item A, item B] etc. 
            for agent in cycle:
                agent_cycle_bundles.append(rotated_allocations[agent]) # same as before for now. agent 0 = [item A, item B] etc.

            for i, agent in enumerate(cycle): # index 0 : agent 0, in cycle [0,1,2]
                next_agent_index = (i + 1) % len(cycle) # get the next agent, prevent overflow
                rotated_allocations[agent] = agent_cycle_bundles[next_agent_index] # agent 0, now has agent 1's bundle
        
        return rotated_allocations
    
    def visualize(self, title: str = "Envy Graph", figsize: Tuple[int, int] = (8, 6)):
        """Visualize the envy graph."""
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                               node_size=1000, alpha=0.7)
        
        # Draw edges with envy amounts as labels
        nx.draw_networkx_edges(self.graph, pos, edge_color='red', 
                               arrows=True, arrowsize=20, alpha=0.6)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, 
                                {i: f"Agent {i}" for i in range(self.num_agents)})
        
        # Draw edge labels (envy amounts)
        edge_labels = {}
        for i, j, data in self.graph.edges(data=True):
            if 'envy_amount' in data:
                edge_labels[(i, j)] = f"{data['envy_amount']:.1f}"
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def get_envy_statistics(self) -> Dict:
        """Get statistics about envy in the current allocation."""
        return {
            'total_envy_edges': len(self.graph.edges()),
            'agents_with_envy': len([n for n in self.graph.nodes() 
                                     if self.graph.out_degree(n) > 0]),
            'envied_agents': len([n for n in self.graph.nodes() 
                                  if self.graph.in_degree(n) > 0]),
            'sources': self.get_sources(),
            'sinks': self.get_sinks(),
            'has_cycles': self.has_cycles(),
            'num_cycles': len(self.get_cycles()),
            'max_envy_amount': max([data.get('envy_amount', 0) 
                                     for _, _, data in self.graph.edges(data=True)], 
                                     default=0)
        }
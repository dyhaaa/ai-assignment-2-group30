import heapq
from typing import Dict, List, Set, Tuple
from Map_Generation import Map, direction

class Node:
    def __init__(self, position: Tuple[int, int, int], g_cost: float = float('inf'), h_cost: float = 0):
        self.position = position
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Cost from current node to goal
        self.f_cost = g_cost + h_cost  # Total cost
        self.parent = None

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def get_neighbors(position: Tuple[int, int, int], game_map: Map) -> List[Tuple[int, int, int]]:
    """Get valid neighboring positions for a given position."""
    neighbors = []
    for dir_vec in direction.values():
        new_pos = (
            position[0] + dir_vec[0],
            position[1] + dir_vec[1],
            position[2] + dir_vec[2]
        )
        if new_pos in game_map.hex_map and game_map.hex_map[new_pos].get("tile") != "obstacle":
            neighbors.append(new_pos)
    return neighbors

def calculate_heuristic(pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> float:
    """Calculate the Manhattan distance between two positions in the hexagonal grid."""
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])) / 2

def a_star_search(game_map: Map, start: Tuple[int, int, int], goal: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """
    A* search algorithm implementation for hexagonal grid.
    Returns the path from start to goal if one exists, otherwise returns an empty list.
    """
    # Initialize open and closed sets
    open_set: List[Node] = []
    closed_set: Set[Tuple[int, int, int]] = set()
    
    # Create the starting node
    start_node = Node(start, 0, calculate_heuristic(start, goal))
    heapq.heappush(open_set, start_node)
    
    # To keep track of all the nodes
    node_dict: Dict[Tuple[int, int, int], Node] = {start: start_node}
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.position == goal:
            # Reconstruct path
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse the path to get start->goal
        
        closed_set.add(current.position)
        
        # Checks all neighbors
        for neighbor_pos in get_neighbors(current.position, game_map):
            if neighbor_pos in closed_set:
                continue
                
            # Calculate new g_cost
            new_g_cost = current.g_cost + 1  # Assuming each step costs 1
            
            
            if neighbor_pos not in node_dict:
                neighbor = Node(neighbor_pos)
                node_dict[neighbor_pos] = neighbor
            else:
                neighbor = node_dict[neighbor_pos]
                
            if new_g_cost < neighbor.g_cost:
                neighbor.g_cost = new_g_cost
                neighbor.h_cost = calculate_heuristic(neighbor_pos, goal)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = current
                
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)
    
    return []  

def find_path(game_map: Map, start: Tuple[int, int, int], goal: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """
    Wrapper function to find path using A* search.
    Returns the path from start to goal if one exists, otherwise returns an empty list.
    """
    return a_star_search(game_map, start, goal) 

     while open_set:
        current = heapq.heappop(open_set)
        
        if current.position == goal:
            # Reconstruct path
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse the path to get start->goal
        
        closed_set.add(current.position)
        
        # Checks all neighbors
        for neighbor_pos in get_neighbors(current.position, game_map):
            if neighbor_pos in closed_set:
                continue
                
            # Calculate new g_cost
            new_g_cost = current.g_cost + 1  # Assuming each step costs 1
            
            
            if neighbor_pos not in node_dict:
                neighbor = Node(neighbor_pos)
                node_dict[neighbor_pos] = neighbor
            else:
                neighbor = node_dict[neighbor_pos]
                
            if new_g_cost < neighbor.g_cost:
                neighbor.g_cost = new_g_cost
                neighbor.h_cost = calculate_heuristic(neighbor_pos, goal)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = current
                
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)
    
    return []  

def find_path(game_map: Map, start: Tuple[int, int, int], goal: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """
    Wrapper function to find path using A* search.
    Returns the path from start to goal if one exists, otherwise returns an empty list.
    """
    return a_star_search(game_map, start, goal) 
from Map_Generation import Map
from Astar_Algorithm import find_path

def test_astar_learning():
    print("Starting test_astar_learning...")
    game_map = Map()
    start = (0, 0, 0)
    goal = (5, -2, -3)

    known_traps = set()
    known_rewards = set()

    for attempt in range(1, 99):
        print(f"\n--- Attempt {attempt} ---")
        path = find_path(game_map, start, goal, known_traps, known_rewards)
        if not path:
            print("No path found!")
            break
        print(f"Path length: {len(path)}")
        found_trap = False
        found_reward = False
        for i, pos in enumerate(path):
            tile_type = game_map.hex_map[pos].get("tile", "unknown")
            print(f"Step {i}: {pos} (Tile: {tile_type})")
            if tile_type == "trap" and pos not in known_traps:
                print("  Encountered a trap! Now will avoid this tile in future runs.")
                known_traps.add(pos)
                found_trap = True
            if tile_type == "reward" and pos not in known_rewards:
                print("  Encountered a reward! Now will prefer this tile in future runs.")
                known_rewards.add(pos)
                found_reward = True
            if tile_type == "treasure":
                collected_treasure += 1;
        if not found_trap and not found_reward:
            print("  No new traps or rewards encountered on this path.")
            break
        elif collected_treasure == 4:
            print("found most optimal path")
            break

if __name__ == "__main__":
    test_astar_learning() 

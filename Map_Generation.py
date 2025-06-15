'''
NOTE:
the coordinates for cube is (q,r,s), where q is up and down (originally east and west, but for simplicity, we say up and down); 
r is northeast and southwest (/); s is northwest and southeast (backslash)
r is northeast and southwest (/); s is northwest and southeast (\)
We must ensure that q + r + s = 0 so when one coord is +1, there must be another to subtract 1 to ensure that it equals 0.

For flat-top hexagons:
Up: q = 0, r - 1, s + 1
Down: q = 0, r + 1, s - 1
NE: q + 1, r - 1, s = 0
SW: q - 1, r + 1, s = 0
NW: q - 1, r = 0, s + 1
SE: q + 1, r = 0, s - 1

'''

# Cube direction vectors
# Coordinates kept in tuples as to not allow any values changing mid execution
# Would be useful for the search algorithm, so I kept it outside of the Map class (Intended to be a global variable in the main file)
direction = {

    "up" : (0, -1, 1),
    "down" : (0, 1, -1),
    "NE" : (1, -1, 0),
    "SW" : (-1, 1, 0),
    "NW" : (-1, 0, 1),
    "SE" : (1, 0 , -1)

}

class Map:

    def __init__(self):
        # Main map variable. Stores all the hexagon tiles' coordinates
        self.hex_map = {}

        # Used to help alternate between Northeast and Southeast. Northeast starts first as shown in the map image given
        # This will help generate the staggered rows
        self.NE_SE_cycle = ["NE","SE"]

        # When initialized, we automatically generate an empty map
        self.generate_empty_map()

        # Initialize the starting coordinates (0,0,0) to be the entry tile
        self.set_tile((0, 0, 0), {"tile": "entry"})

        # A tuple containing coordinates for all existing obstacles on the map
        self.obstacle_coords = (
            (0, 3, -3), 
            (2, 1, -3), 
            (3, 1, -4),
            (4, 0, -4),
            (4, 2, -6),
            (6, 1, -7),
            (6, 0, -6),
            (7, 0, -7),
            (8, -3, -5)
        )

        # We fill in the obstacles inside the empty map
        self.fill_map(self.obstacle_coords, "obstacle")

    # Primary function to generate coordinates for new tiles
    # Parameter meaning: current_hex is the hexagon the player is currently in. dir_vec is the directional vector, it retrieves the coordinates for the direction you intend to go.
    def add_new_tile_coords(self, current_hex : tuple, dir_vec : tuple) -> tuple:
        return (current_hex[0] + dir_vec[0], current_hex[1] + dir_vec[1], current_hex[2] + dir_vec[2]) # We add both coordinates together. e.g. (0,0,1) + (1,0,-1) = (1,0,0)
    
    # Function to swap the direction coordinates in the list
    def swap_direction(self, dir_list : list) -> None:
        temp_var = dir_list[0] # Saving the first element in the list into a temporary variable

        dir_list.pop(0) # remove the first element in the list

        dir_list.append(temp_var) # Put the first element at back of the list, allowing the second element to become first

    # Primary function to generate a new empty hexagonal map
    def generate_empty_map(self) -> None:

        # Set the current tile coordinate to the starting tile (0,0,0)
        current_tile = (0,0,0)

        # Set the current column tile to be the starting tile at first
        current_col_tile = current_tile

        # Set the current row tile to be the starting tile at first
        current_row_tile = current_tile

        # Generate 6 columns
        for col in range(6):
            # Each new column will be added first
            self.hex_map[current_col_tile] = {"tile" : "empty"}

            # Generate 9 rows. We don't generate 10 rows because we already have the starting column added
            for row in range(9):
                next_row_tile = self.add_new_tile_coords(current_row_tile, direction[self.NE_SE_cycle[0]]) # Generating coordinates for the next tile in the row
                self.hex_map[next_row_tile] = {"tile" : "empty"} # Add the new tile into the dictionary and declaring the tile empty
                current_row_tile = next_row_tile # Set the current row as the next one so we can continuously go down the row
                self.swap_direction(self.NE_SE_cycle) # After creating a tile, we swap the direction to get the staggered hexagon rows
            
            # After generating the row, we update the column to move to the next one
            next_col = self.add_new_tile_coords(current_col_tile, direction["down"])
            current_col_tile = next_col # Move the current column to the next one
            current_row_tile = next_col # Reset the current row to go to the next column

            # Swap the direction again as when we move to the next column, we want to reset it back to the NE-SE state
            self.swap_direction(self.NE_SE_cycle)
    
    # A function that only sets one tile with a given tile type
    def set_tile(self, tile_coord : tuple, tile_type):
        self.hex_map[tile_coord] = tile_type
    
    # A function to add features/conditions into multiple tiles of the map
    def fill_map(self, tile_coords : tuple[tuple], tile_type):
        for coordinate in tile_coords:
            self.hex_map[coordinate]["tile"] = tile_type

'''
For debugging. If you would like to see the coordinates, remove the three single quotation marks.

new_map = Map()

print(new_map.hex_map, '\n')
print("total amount of tiles: ", len(new_map.hex_map))
'''
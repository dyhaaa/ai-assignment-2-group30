from copy import deepcopy
from enum import Enum
import pygame
import math

# Cube direction vectors, used in calculating the movement coordinates.
# Would be useful for the search algorithm, so I kept it outside of the Map class (Intended to be a global variable in the main file)
direction = {

    "up": (0, -1, 1),
    "down": (0, 1, -1),
    "NE": (1, -1, 0),
    "SW": (-1, 1, 0),
    "NW": (-1, 0, 1),
    "SE": (1, 0, -1)

}

class TileType(Enum):
    EMPTY = 1
    OBSTACLE = 2
    TREASURE = 3
    TRAP1 = 4
    TRAP2 = 5
    TRAP3 = 6
    TRAP4 = 7
    REWARD1 = 8
    REWARD2 = 9


class TrapOrReward:
    def __init__(self, coordinate, trap_type: TileType, active=True):
        self.coordinate = coordinate  # Coords from the Map
        self.trap_type = trap_type  # 'Trap1', 'Trap2', etc.
        self.active = active  # Setting to Activate trap

    def __str__(self):
        return f"{self.coordinate}: {self.trap_type.name}"

    # Check to Apply the actual trap to the player
    def apply(self, player):
        if not self.active:
            return

        if self.trap_type == TileType.TRAP1:
            player.setEnergyCost(player.getEnergyCost() * 2)

        elif self.trap_type == TileType.TRAP2:
            player.setStepCost(player.getStepCost() * 2)

        elif self.trap_type == TileType.TRAP3:
            player.trap3()  # Uses Adams Trap

        elif self.trap_type == TileType.TRAP4:
            self.CanCollectTreasure = False

        elif self.trap_type == TileType.REWARD1:
            player.setEnergyCost(player.getEnergyCost() / 2)

        elif self.trap_type == TileType.REWARD2:
            player.setStepCost(player.getStepCost() / 2)

        elif self.trap_type == TileType.TREASURE:
            player.collectTreasure()

        self.active = False


class Player:

    def __init__(self, history: list[tuple[int, int, int]], position: tuple[int, int, int], tileStatus: list[TrapOrReward], treasure: int, step: int, energy: int,
                 stepCost: int, energyCost: int):
        self.history = history
        self.position = position
        self.tileStatus = tileStatus
        self.treasure = treasure
        self.step = step
        self.energy = energy
        self.stepCost = stepCost
        self.energyCost = energyCost
        self.canCollectTreasure = True  # Added by Karl Need this for Trap 4

    # toString method
    def __str__(self):
        num = 1
        posstr = ""
        for pos in self.history:
            posstr += (f"\n{num}." + str(pos))
            num += 1
        return f"History: {posstr}\nCurrent Pos:{self.position}\nSteps:{self.step}, Energy:{self.energy}\nSteps Cost:{self.stepCost}, Energy Cost:{self.energyCost}\nTreasure:{self.treasure}\n"

    # Setters and Getters
    def getHistory(self):
        return self.history

    def getPosition(self):
        return self.position

    def getTileStatus(self):
        return self.position

    def getTreasure(self):
        return self.treasure

    def getStep(self):
        return self.step

    def getEnergy(self):
        return self.energy

    def getStepCost(self):
        return self.stepCost

    def getEnergyCost(self):
        return self.energyCost

    def setHistory(self, new: list[tuple[int, int, int]]):
        self.history = new

    def setPosition(self, new: tuple[int, int, int]):
        self.position = new

    def setTileStatus(self, new: list[TrapOrReward]):
        self.tileStatus = new

    def setTreasure(self, new: int):
        self.treasure = new

    def setStep(self, new: float):
        self.step = new

    def setEnergy(self, new: float):
        self.energy = new

    def setStepCost(self, new: float):
        self.stepCost = new

    def setEnergyCost(self, new: float):
        self.energyCost = new

    # Class Methods
    # Stores the current position in history then sets the position in the parameters to the new one, also adds the steps and energy based on stepCost and energyCost
    def moveTile(self, target: tuple[int, int, int]):
        # Check weather tile is valid
        self.history.append(self.position)
        self.position = target
        self.step += self.stepCost
        self.energy += self.energyCost
        for tile in self.tileStatus:
            if tile.coordinate == target:
                tile.apply(self)
                
     # Testing the functionality of history

    def trap3(self):
        curQ, curR, curS = self.position
        q, r, s = self.history[-2]
        x, y, z = self.history[-1]

        # Determine direction of last movement
        dq = x - q
        dr = y - r
        ds = z - s

        # Push backward from current tile
        new_q = curQ - 2 * dq
        new_r = curR - 2 * dr
        new_s = curS - 2 * ds

        if new_q + new_r + new_s != 0:
            print("Invalid push-back position!")
            return

        print(f"Trap3 activated! Moving back from {self.position} to ({new_q}, {new_r}, {new_s})")
        self.history.append(self.position)
        self.position = new_q, new_r, new_s

    # Method for Collecting Treasure Also used to Checking Treasure
    def collectTreasure(self):
        # If Trap 4 hasnt been hit use this
        if self.canCollectTreasure:
            self.treasure += 1
            print("Treasure collected!")
        else:
            print("No More Treasure can be Collected. Trap 4 Activated.")


class Map:

    # A tuple containing coordinates for all existing special hexagons (obstacles, traps, rewards, treasures) on the map
    Obstacle_Coords = (
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

    Trap1_Coords = (
        # Need to leave the comma for it to be tuple of tuple, for the listing to work properly for the coordinate instead of being split up
        (8, -2, -6),
    )
    Trap2_Coords = (
        (1, 0, -1),
        (2, 3, -5)
    )
    Trap3_Coords = (
        (6, -2, -4),
        (5, 0, -5)
    )
    Trap4_Coords = (
        # Need to leave the comma for it to be tuple of tuple, for the listing to work properly for the coordinate instead of being split up
        (3, -1, -2),
    )
    Reward1_Coords = (
        (4, -2, -2),
        (1, 2, -3)
    )
    Reward2_Coords = (
        (5, 2, -7),
        (7, -2, -5)
    )
    Treasure_Coords = (
        (4, -1, -3),
        (7, -1, -6),
        (9, -2, -7),
        (3, 2, -5)
    )

    def __init__(self):
        # Main map variable. Stores all the hexagon tiles' coordinates
        self.hex_map = {}

        # Used to help alternate between Northeast and Southeast. Northeast starts first as shown in the map image given
        # This will help generate the staggered rows
        self.NE_SE_cycle = ["NE", "SE"]

        # When initialized, we automatically generate an empty map
        self.generate_empty_map()

        # We fill in the special hexagons inside the empty map
        self.fill_map(self.Obstacle_Coords, TileType.OBSTACLE)
        self.fill_map(self.Trap1_Coords, TileType.TRAP1)
        self.fill_map(self.Trap2_Coords, TileType.TRAP2)
        self.fill_map(self.Trap3_Coords, TileType.TRAP3)
        self.fill_map(self.Trap4_Coords, TileType.TRAP4)
        self.fill_map(self.Reward1_Coords, TileType.REWARD1)
        self.fill_map(self.Reward2_Coords, TileType.REWARD2)
        self.fill_map(self.Treasure_Coords, TileType.TREASURE)

    # toString Method
    def __str__(self):
        string = "Coordinates : Tile Type"
        for key, tile in self.hex_map.items():
            string += f"\n{key}: {tile.name}"
        return string

    # Primary function to generate coordinates for new tiles
    # Parameter meaning: current_hex is the hexagon the player is currently in. dir_vec is the directional vector, it retrieves the coordinates for the direction you intend to go.
    def add_new_tile_coords(self, current_hex: tuple, dir_vec: tuple) -> tuple:
        # We add both coordinates together. e.g. (0,0,1) + (1,0,-1) = (1,0,0)
        return (current_hex[0] + dir_vec[0], current_hex[1] + dir_vec[1], current_hex[2] + dir_vec[2])

    # Function to swap the direction coordinates in the list
    def swap_direction(self, dir_list: list) -> None:
        # Saving the first element in the list into a temporary variable
        temp_var = dir_list[0]

        dir_list.pop(0)  # remove the first element in the list

        # Put the first element at back of the list, allowing the second element to become first
        dir_list.append(temp_var)

    # Primary function to generate a new empty hexagonal map
    def generate_empty_map(self) -> None:

        # Set the current tile coordinate to the starting tile (0,0,0)
        current_tile = (0, 0, 0)

        # Set the current column tile to be the starting tile at first
        current_col_tile = current_tile

        # Set the current row tile to be the starting tile at first
        current_row_tile = current_tile

        # Generate 6 columns
        for col in range(6):
            # Each new column will be added first
            self.hex_map[current_col_tile] = TileType.EMPTY

            # Generate 9 rows. We don't generate 10 rows because we already have the starting column added
            for row in range(9):
                # Generating coordinates for the next tile in the row
                next_row_tile = self.add_new_tile_coords(
                    current_row_tile, direction[self.NE_SE_cycle[0]])
                # Add the new tile into the dictionary and declaring the tile empty
                self.hex_map[next_row_tile] = TileType.EMPTY
                # Set the current row as the next one so we can continuously go down the row
                current_row_tile = next_row_tile
                # After creating a tile, we swap the direction to get the staggered hexagon rows
                self.swap_direction(self.NE_SE_cycle)

            # After generating the row, we update the column to move to the next one
            next_col = self.add_new_tile_coords(
                current_col_tile, direction["down"])
            current_col_tile = next_col  # Move the current column to the next one
            current_row_tile = next_col  # Reset the current row to go to the next column

            # Swap the direction again as when we move to the next column, we want to reset it back to the NE-SE state
            self.swap_direction(self.NE_SE_cycle)

    # A function to add features/conditions into multiple tiles of the map
    # Parameter meaning: tile_coords is a tuple containing multiple coordinates that need to be changed. tile_type is the type of tile the chosen hexagons will be.
    def fill_map(self, tile_coords: tuple, tile_type: TileType):
        for coordinate in tile_coords:
            self.hex_map[coordinate] = tile_type

    # A function to return a list of valid coordinates the player can go to
    # Parameter meaning: cur_pos is current_position of the player, takes in the current tile coordinate the player is in
    def check_valid_tiles(self, cur_pos: tuple) -> list[tuple]:
        # Checking to see if the coordinates passed into the argument exists in the map
        # if it doesn't, we throw an exception error message
        if (cur_pos not in self.hex_map):
            raise Exception(
                f"The position: {cur_pos}, is invalid. Cannot be found in the map.")
        else:
            # List that will hold all the valid tiles the player can move to
            valid_tiles = []

            # Dictionary that contains all hexagons that surround the player's current position
            surrounding_tiles = {}

            # Appending the dictionary with the surrounding tile coords
            surrounding_tiles["up"] = self.add_new_tile_coords(
                cur_pos, direction['up'])
            surrounding_tiles["down"] = self.add_new_tile_coords(
                cur_pos, direction['down'])
            surrounding_tiles["NE"] = self.add_new_tile_coords(
                cur_pos, direction['NE'])
            surrounding_tiles["NW"] = self.add_new_tile_coords(
                cur_pos, direction['NW'])
            surrounding_tiles["SE"] = self.add_new_tile_coords(
                cur_pos, direction['SE'])
            surrounding_tiles["SW"] = self.add_new_tile_coords(
                cur_pos, direction['SW'])

            # dictionary containing the pairing of coordinates q and r
            # Mainly used for checking the border of both top and bottom rows, excluding the columns at q = 0 and q = 9
            top_row_pair = {1: -1, 2: -1, 3: -2,
                            4: -2, 5: -3, 6: -3, 7: -4, 8: -4}
            bottom_row_pair = {1: 4, 2: 4, 3: 3, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1}

            # Assigning coordinate position value to respective variable
            q = cur_pos[0]
            r = cur_pos[1]

            # Checking to see if the player's current position is in the border of the map
            # Apply necessary changes if the condition is met
            # Checking for left column excluding corners
            if (q == 0 and (r > 0 and r < 5)):
                surrounding_tiles.pop('NW')
                surrounding_tiles.pop('SW')
            # Checking for right column excluding corners
            elif (q == 9 and (r > -5 and r < 0)):
                surrounding_tiles.pop('NE')
                surrounding_tiles.pop('SE')
            # Checking for NE top row
            elif ((q % 2 != 0) and (q > 0 and q < 9) and ((q in top_row_pair) and top_row_pair[q] == r)):
                surrounding_tiles.pop('up')
                surrounding_tiles.pop('NW')
                surrounding_tiles.pop('NE')
            # Checking for SE top row
            elif ((q % 2 == 0) and (q > 0 and q < 9) and ((q in top_row_pair) and top_row_pair[q] == r)):
                surrounding_tiles.pop('up')
            # Checking for NE bottom row
            elif ((q % 2 != 0) and (q > 0 and q < 9) and ((q in bottom_row_pair) and bottom_row_pair[q] == r)):
                surrounding_tiles.pop('down')
            # Checking for SE bottom row
            elif ((q % 2 == 0) and (q > 0 and q < 9) and ((q in bottom_row_pair) and bottom_row_pair[q] == r)):
                surrounding_tiles.pop('down')
                surrounding_tiles.pop('SW')
                surrounding_tiles.pop('SE')
            # Checking for top left corner
            elif (q == 0 and r == 0):
                surrounding_tiles.pop('up')
                surrounding_tiles.pop('NW')
                surrounding_tiles.pop('SW')
            # Checking for bottom left corner
            elif (q == 0 and r == 5):
                surrounding_tiles.pop('down')
                surrounding_tiles.pop('NW')
                surrounding_tiles.pop('SW')
                surrounding_tiles.pop('SE')
            # Checking for top right corner
            elif (q == 9 and r == -5):
                surrounding_tiles.pop('up')
                surrounding_tiles.pop('NW')
                surrounding_tiles.pop('NE')
                surrounding_tiles.pop('SE')
            # Checking for bottom right corner
            elif (q == 9 and r == 0):
                surrounding_tiles.pop('down')
                surrounding_tiles.pop('SE')
                surrounding_tiles.pop('NE')

            # The remaining valid tiles after checking if it's a border tile will be checked if it is an obstacle or not
            # To not mess with the dictionary since we're going to remove elements in it, we will use a copy of list of all keys in the dict
            for tile in list(surrounding_tiles.keys()):
                # Accessing the coordinate from the surrounding_tiles dict
                coord = surrounding_tiles[tile]
                # If the coordinate does not exist
                if coord not in self.hex_map:
                    # We get rid of the coordinate
                    surrounding_tiles.pop(tile)
                # If the coordinate is an obstacle
                elif self.hex_map[coord] == TileType.OBSTACLE:
                    # Remove it from the list since it isn't a valid tile for the player to move into
                    surrounding_tiles.pop(tile)

            # Finally, after filtering, we can return the list of coordinates containing coords that are valid for the player to move to
            for valid_tile_coord in surrounding_tiles.values():
                valid_tiles.append(valid_tile_coord)

            return valid_tiles

# DEBUG


new_map = Map()

print(new_map)
print("total amount of tiles: ", len(new_map.hex_map))
print(new_map.check_valid_tiles((0, 0, 0)))


#
#
#
# MAP UI
# Constant variables
"""
BACKGROUND_COLOUR = (220, 220, 220)
HEX_DEFAULT_COLOUR = (255, 255, 255)
HEX_RADIUS = 50  # Size of hexagon


class HexagonTile:
    # Class for a hexagon tile
    def __init__(self, x, y, radius, colour=HEX_DEFAULT_COLOUR, icon=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.icon = icon

    def get_corners(self):
        # Calculate vertices of hexagon
        vertices = []
        for i in range(6):
            angle_degree = 60 * i
            angle_radian = math.radians(angle_degree)
            point_x = self.x + self.radius * math.cos(angle_radian)
            point_y = self.y + self.radius * math.sin(angle_radian)
            vertices.append((point_x, point_y))
        return vertices

    def draw(self, screen, text):
        # Draw hexagon
        pygame.draw.polygon(screen, self.colour, self.get_corners())
        # Draw outline
        pygame.draw.polygon(screen, (0, 0, 0), self.get_corners(), 2)

        # Draw icon if needed
        if self.icon:
            symbol = text.render(self.icon, True, (255, 255, 255))
            symbol_rect = symbol.get_rect(center=(self.x, self.y-5))
            screen.blit(symbol, symbol_rect)

    def highlight_hex(self, screen, border_colour, thickness):
        # Draw border around hexagon
        pygame.draw.lines(screen, border_colour, closed=True,
                          points=self.get_corners(), width=thickness)


def cube_to_screen(q, r, radius, origin_x=100, origin_y=150, offset_x=0, offset_y=0):
    # Convert cube coordinates to screen coordinates
    # Convert cube to axial coordinates
    x = q
    y = r

    # Convert axial to screen coordinates
    screen_x = x * radius * 1.67 + origin_x + offset_x
    screen_y = y * radius * 2 + (x * radius) + origin_y + offset_y

    return (screen_x, screen_y)


def draw_map(hex_map, special_hexagons=None, radius=HEX_RADIUS, offset_x=0, offset_y=0):
    # Hexagons list
    hexes = []

    for coord, tile_data in hex_map.items():  # tile_data and s not used, but have to be unpacked
        q, r, s = coord

        # Convert cube coordinates to screen position
        x, y = cube_to_screen(
            q, r, radius, offset_x=offset_x, offset_y=offset_y)

        # Check if hexagon tile is special
        special = next(
            (hex for hex in special_hexagons if hex['coord'] == coord), None)

        # Build tile and append to list of hexes
        tile = HexagonTile(
            x, y, radius,
            colour=special['colour'] if special else HEX_DEFAULT_COLOUR,
            icon=special['icon'] if special else None
        )
        hexes.append(tile)

    return hexes


def is_cursor_in_hex(x, y, hex_x, hex_y, radius):
    # Check distance
    distance_x = x - hex_x
    distance_y = y - hex_y
    # Get distance of cursor from hex (triangle pythagorean theorem)
    distance = math.sqrt(distance_x**2 + distance_y**2)
    return distance <= radius


def make_special_hexagons(map):

    # Special hexagons list, starting with entry tile
    special_hexagons = [
        {
            'coord': (0, 0, 0),
            'colour': (0, 180, 255),
            'icon': '↘',  # Entry tile
            'description': 'Starting Point'
        }
    ]

    # Add special hexagons from map
    # List of tuples containing the coordinate list and their properties
    coord_lists = [
        (map.Obstacle_Coords, (100, 100, 100), None,
         'Impassable obstacle. A random giant boulder that just happens to be here.'),
        (map.Trap1_Coords, (200, 150, 255), '⊖',
         'This trap will increase the gravity of the world. Every step you take will consume double the energy as previous.'),
        (map.Trap2_Coords, (200, 150, 255), '⊕',
         'This trap will decrease your speed. You will take double the steps to move to the adjacent cell.'),
        (map.Trap3_Coords, (200, 150, 255), '⊗',
         'This trap will move you two cells away following your last movement direction.'),
        (map.Trap4_Coords, (200, 150, 255), '⊘',
         'This trap will remove all treasures that have not been collected. All treasures that are collected will not be affected.'),
        (map.Reward1_Coords, (80, 200, 170), '⊞',
         'This reward will decrease the gravity of the world. Every step you take will consume half the energy as previous.'),
        (map.Reward2_Coords, (80, 200, 170), '⊠',
         'This reward will increase your speed. You will take half the steps to move to the adjacent cell.'),
        (map.Treasure_Coords, (255, 180, 20), None,
         'Shiny, shimmering, splendid treasure. Just holding it gives you a big dopamine boost.')
    ]

    # Single loop to process all coordinates and their properties
    for coord_list, colour, icon, description in coord_lists:
        for coord in coord_list:
            special_hexagons.append({
                'coord': coord,
                'colour': colour,
                'icon': icon,
                'description': description
            })

    return special_hexagons


def draw_popup(screen, cursor_pos, selected_hex, font):
    # Popup position
    popup_x = cursor_pos[0] + 10
    popup_y = cursor_pos[1] + 10

    # Popup box
    popup_width = 300
    popup_height = 200
    popup_rect = pygame.Rect(
        popup_x, popup_y, popup_width, popup_height)

    # Draw background
    pygame.draw.rect(screen, selected_hex['colour'], popup_rect)
    # Draw border
    pygame.draw.rect(screen, (50, 50, 50), popup_rect, 2)

    # Draw description text
    description = selected_hex['description']
    description_surface = font.render(
        description, True, (255, 255, 255))
    description_rect = description_surface.get_rect(
        center=(popup_x + popup_width//2, popup_y + popup_height//2))
    screen.blit(description_surface, description_rect)


def main():
    # Initialise screen for display
    pygame.init()
    screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Treasure Hunt In a Virtual World")
    text = pygame.font.Font('Arial-Unicode-MS.ttf', 50)
    text_desc = pygame.font.Font('Arial-Unicode-MS.ttf', 20)

    # Initialize the map
    game_map = Map()
    # Make special hexagons list
    special_hexagons = make_special_hexagons(game_map)
    # List map
    hex_tiles = draw_map(game_map.hex_map, special_hexagons, HEX_RADIUS)

    # Variables
    # For dragging map
    map_offset_x = 0
    map_offset_y = 0
    dragging = False
    drag_start_pos = (0, 0)

    # For hexagon highlighting and popups
    show_popup = False
    selected_hex = None
    cursor_pos = (0, 0)

    running = True
    while running:
        # Draw map
        screen.fill(BACKGROUND_COLOUR)
        for tile in hex_tiles:
            tile.draw(screen, text)

        # Get cursor position
        cursor_pos = pygame.mouse.get_pos()

        # Check if hovering over special hexagon
        for hex_tile in hex_tiles:
            for hex_info in special_hexagons:
                # Get cube coordinates
                q, r, s = hex_info['coord']
                # Convert cube coordinates to screen coordinates
                x, y = cube_to_screen(
                    q, r, HEX_RADIUS, offset_x=map_offset_x, offset_y=map_offset_y)
                # Check if mouse over special hexagon, if so then highlight hexagon tile
                if is_cursor_in_hex(cursor_pos[0], cursor_pos[1], hex_tile.x, hex_tile.y, hex_tile.radius) and (hex_tile.x, hex_tile.y) == (x, y):
                    hex_tile.highlight_hex(screen, (255, 255, 255), 3)
                    # Check if hexagon clicked, if so then show popup
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        selected_hex = hex_info
                        show_popup = True
                    else:
                        show_popup = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check if holding left mouse button (event.button == 1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                drag_start_pos = pygame.mouse.get_pos()

            # Check if released left mouse button
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            # While holding down left mouse button and moving mouse
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - drag_start_pos[0]
                dy = mouse_y - drag_start_pos[1]
                map_offset_x += dx
                map_offset_y += dy
                drag_start_pos = (mouse_x, mouse_y)
                # Redraw map with updated offset
                hex_tiles = draw_map(
                    game_map.hex_map, special_hexagons, HEX_RADIUS, map_offset_x, map_offset_y)

        # Draw popup
        if show_popup and selected_hex:
            draw_popup(screen, cursor_pos, selected_hex, text_desc)

        # Doesn't flip like a shape, just updates the display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
"""

startingTiles = []
tileCoords = [Map.Trap1_Coords, Map.Trap2_Coords, Map.Trap1_Coords,
              Map.Trap2_Coords, Map.Reward1_Coords, Map.Reward2_Coords, Map.Treasure_Coords]
tileTypes = [TileType.TRAP1, TileType.TRAP2, TileType.TRAP3,
             TileType.TRAP4, TileType.REWARD1, TileType.REWARD2, TileType.TREASURE]

for i in range(len(tileTypes)):
    for q, r, s in tileCoords[i]:
        startingTiles.append(TrapOrReward((q, r, s), tileTypes[i]))

def calcShortest(pos1: tuple[int, int, int], pos2: tuple[int, int, int]) -> float:
    
    #Calculate the Manhattan distance between two positions in the hexagonal grid
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])) / 2
    
def calcHscore(plyr: Player):
    hscore = 0
    treasures = []
    tileStatus = plyr.tileStatus
    for tile in tileStatus:
        if (tile.trap_type == TileType.TREASURE) & tile.active:
            treasures.append(tile)
    for treasure in treasures:
        hscore += calcShortest(plyr.getPosition(), treasure.coordinate)
    if not plyr.canCollectTreasure: 
        return math.inf
    return hscore * plyr.getEnergyCost() * plyr.getStepCost()

def calcFScore(player: Player):
    gfunc = player.energy
    hfunc = calcHscore(player)
    
    return gfunc + hfunc

# Change this to modify initial values
STARTING_PLAYER = Player([], (0, 0, 0), startingTiles, 0, 0, 0, 1, 2)



pioneers = []
pioneers.append(STARTING_PLAYER)
optimal = math.inf


while len(pioneers) != 0:
    
    #Populate
    lead = pioneers[0] #Take the least fscore
    children = []
    for path in new_map.check_valid_tiles(lead.position):
        child = deepcopy(lead)
        child.moveTile(path)
        if new_map.hex_map[path] != TileType.EMPTY:
            for tile in child.tileStatus:
                if tile.coordinate == path:
                    tile.apply(child)
        if optimal >= calcFScore(child):
            children.append(child)
    del pioneers[0]
            
    #Goal Test
    for candidate in children:
        if candidate.treasure == 4:
            if calcFScore(candidate) < optimal:
                optimal = calcFScore(candidate)
                goal = deepcopy(candidate)
            del candidate
        else:
            pioneers.append(candidate)

    #Cull Pioneers
    for plyr in pioneers:
        if optimal <= calcFScore(plyr):
            if plyr in pioneers:
                pioneers.remove(plyr)

    #Sort
    pioneers.sort(key= lambda x: calcFScore(x), reverse=False)
    if len(pioneers) != 0:
        print(pioneers[0])
        print(calcFScore(pioneers[0]))
        print(len(pioneers))
        print(optimal)

print(goal)
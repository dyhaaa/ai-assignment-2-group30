import pygame
import math
from Map_Generation import Map

#
#
#
# MAP UI

# Constant variables

background_colour = (200, 200, 200)
hex_default_colour = (255, 255, 255)
hex_radius = 50  # Size of hexagon


class HexagonTile:
    # Class for a hexagon tile
    def __init__(self, x, y, radius, colour=hex_default_colour, icon=None):
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
            symbol_rect = symbol.get_rect(center=(self.x, self.y))
            screen.blit(symbol, symbol_rect)


def cube_to_screen(q, r, radius, origin_x=100, origin_y=150):
    # Convert cube coordinates to screen coordinates
    # Convert cube to axial coordinates
    x = q
    y = r

    # Convert axial to screen coordinates
    screen_x = x * radius * 1.67 + origin_x
    screen_y = y * radius * 2 + (x * radius) + origin_y

    return (screen_x, screen_y)


def draw_map(hex_map, special_hexagons=None, radius=hex_radius):
    hexes = []

    for coord, tile_data in hex_map.items():
        q, r, s = coord

        # Convert cube coordinates to screen position
        x, y = cube_to_screen(q, r, radius)

        # Check if hexagon tile is special
        special = next(
            (hex for hex in special_hexagons if hex['coord'] == coord), None)

        tile = HexagonTile(
            x, y, radius,
            colour=special['colour'] if special else hex_default_colour,
            icon=special['icon'] if special else None
        )
        hexes.append(tile)

    return hexes


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Treasure Hunt In a Virtual World")
    text = pygame.font.SysFont('Arial', 30)

    # Initialize the map
    game_map = Map()

    # Special hexagons list to be put on map, created empty
    special_hexagons = []

    # Add entry point tile
    special_hexagons.append(
        {
            'coord': (0, 0, 0),  # Entry tile
            'colour': (0, 180, 255),
            'icon': 'Entry'
        }
    )

    # Add special hexagons from map
    # List of tuples containing the coordinate list and their properties
    coord_lists = [
        (game_map.obstacle_coords, (100, 100, 100), None),
        (game_map.Trap1_Coords, (200, 150, 255), '-'),
        (game_map.Trap2_Coords, (200, 150, 255), '+'),
        (game_map.Trap3_Coords, (200, 150, 255), 'x'),
        (game_map.Trap4_Coords, (200, 150, 255), '/'),
        (game_map.Reward1_Coords, (80, 200, 170), '+'),
        (game_map.Reward2_Coords, (80, 200, 170), 'x'),
        (game_map.Treasure, (255, 180, 20), None)
    ]

    # Single loop to process all coordinates and their properties
    for coord_list, colour, icon in coord_lists:
        for coord in coord_list:
            special_hexagons.append({
                'coord': coord,
                'colour': colour,
                'icon': icon
            })

    hex_tiles = draw_map(game_map.hex_map, special_hexagons, hex_radius)

    running = True
    while running:
        screen.fill(background_colour)
        for tile in hex_tiles:
            tile.draw(screen, text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()

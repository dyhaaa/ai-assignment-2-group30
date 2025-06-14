# -*- coding: utf-8 -*-

# ? ! trap, rewards popup uis, player icon, show path history, show chosen best paths

import pygame
import math

background_colour = (200, 200, 200)
hex_default_colour = (255, 255, 255)
hex_radius = 50  # Size of hexagon


class HexagonTile:

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


def draw_map(rows, columns, radius, special_hexagons=None):
    hexes = []
    width = radius * 2
    height = math.sqrt(3) * radius

    for row in range(rows):
        for column in range(columns):
            x = column * (width * 3/4)
            y = row * height - (column % 2) * (height / 2)

            # Check if this position is special
            special = next(
                (hex for hex in special_hexagons if hex['row'] == row and hex['column'] == column), None)

            # Apply special properties or use defaults
            tile = HexagonTile(
                x + 100,
                y + 100,
                radius,
                colour=special['colour'] if special else hex_default_colour,
                icon=special['icon'] if special else None
            )
            hexes.append(tile)

    return hexes


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Treasure Hunt In a Virtual World")
    text = pygame.font.SysFont('Arial', 30)

    # Locations and details of special hexagons
    special_hexagons = [
        {
            'row': 2,
            'column': 8,
            'colour': (200, 120, 220),  # Trap1
            'icon': '-'
        },
        {
            'row': 1,
            'column': 1,
            'colour': (200, 120, 220),  # Trap2a
            'icon': '+'
        },
        {
            'row': 4,
            'column': 2,
            'colour': (200, 120, 220),  # Trap2b
            'icon': '+'
        },
        {
            'row': 1,
            'column': 6,
            'colour': (200, 120, 220),  # Trap3a
            'icon': 'x'
        },
        {
            'row': 3,
            'column': 5,
            'colour': (200, 120, 220),  # Trap3b
            'icon': 'x'
        },
        {
            'row': 1,
            'column': 3,
            'colour': (200, 120, 220),  # Trap4
            'icon': '+'
        },
        {
            'row': 1,
            'column': 4,
            'colour': (255, 180, 0),  # Treasure1
            'icon': None
        },
        {
            'row': 2,
            'column': 2,
            'colour': (100, 100, 100),  # Obstacle1
            'icon': None
        }

    ]

    hex_tiles = draw_map(rows=6, columns=10, radius=hex_radius,
                         special_hexagons=special_hexagons)

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

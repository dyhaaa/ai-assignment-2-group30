# -*- coding: utf-8 -*-

import pygame
import math

background_colour = (50, 50, 50)
hex_default_colour = (200, 200, 200)
hex_radius = 50  # Size of hexagon


class HexagonTile:

    def __init__(self, x, y, radius, colour=hex_default_colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour

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

    def draw(self, screen):
        # Draw hexagon
        pygame.draw.polygon(screen, self.colour, self.get_corners())
        # Draw outline
        pygame.draw.polygon(screen, (0, 0, 0), self.get_corners(), 2)


def draw_map(rows, columns, radius):
    hexes = []
    width = radius * 2
    height = math.sqrt(3) * radius
    for row in range(rows):
        for column in range(columns):
            x = column * (width * 3/4)
            y = row * height - (column % 2) * (height / 2)
            hexes.append(HexagonTile(x + 100, y + 100, radius))
    return hexes


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Treasure Hunt In a Virtual World")

    hex_tiles = draw_map(rows=6, columns=10, radius=hex_radius)

    running = True
    while running:
        screen.fill(background_colour)
        for tile in hex_tiles:
            tile.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()

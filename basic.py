import pygame
import os
import math

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation")

lights = [
    {"pos": (200, 200), "on": False},
    {"pos": (400, 200), "on": False},
    {"pos": (600, 200), "on": False},
    {"pos": (200, 400), "on": False},
    {"pos": (400, 400), "on": False},
    {"pos": (600, 400), "on": False}
]

def load_and_scale_image(filename, target_width):
    image = pygame.image.load(filename)
    original_width, original_height = image.get_size()
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)
    scaled_image = pygame.transform.scale(image, (target_width, target_height))
    return scaled_image

target_width = 50
light_off = load_and_scale_image("light_off.png", target_width)
light_on = load_and_scale_image("light_on.png", target_width)
receiver = load_and_scale_image("receiver.png", target_width)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    original_coords = []

    if os.path.exists("coords.txt"):
        with open("coords.txt", "r") as file:
            coords = file.read().split(",")
            if coords == '':
                continue
            print(coords)
            if coords[0] == '' or coords[1] == '':
                continue
            x, y = float(coords[0]), float(coords[1])
            original_coords.append(x)
            original_coords.append(y)

            min_distance = float("inf")
            nearest_light = None
            for light in lights:
                distance = math.sqrt((light["pos"][0] - x) ** 2 + (light["pos"][1] - y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_light = light

            for light in lights:
                light["on"] = False
            if nearest_light:
                nearest_light["on"] = True

    screen.fill((255, 255, 255))

    for light in lights:
        if light["on"]:
            screen.blit(light_on, (light["pos"][0] - 25, light["pos"][1] - 25))
        else:
            screen.blit(light_off, (light["pos"][0] - 25, light["pos"][1] - 25))

    # print(original_coords)
    screen.blit(receiver, (original_coords[0], original_coords[1]))
    # screen.blit(receiver, (0,0))
    # screen.blit(light_off, (300,0))

    pygame.display.flip()

pygame.quit()



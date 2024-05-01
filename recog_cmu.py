import pygame
import os
import math
import pyaudio
import time
from pocketsphinx import Decoder
import webrtcvad

vad = webrtcvad.Vad()
vad.set_mode(3)  # sensitivity

# PyAudio config
CHUNK = 320
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

config = {
    'hmm': r'C:\Users\ALIENWARE\AppData\Roaming\Python\Python311\site-packages\pocketsphinx\model\en-us\en-us',
    'dict': r'C:\Users\ALIENWARE\AppData\Roaming\Python\Python311\site-packages\pocketsphinx\model\en-us\cmudict-en-us.dict',
    # 'kws_threshold': 1e-20,
    'samprate': RATE
}

decoder = Decoder(config)


# with open('keyphrase.list', 'w') as f:
#     f.write('open\n')


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("灯光控制模拟")

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

# set the decoder with kws
decoder.add_kws('kws_search', 'keyphrase.list')
decoder.activate_search('kws_search')

running = True
decoder.start_utt()
light_timer = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    original_coords = []

    if os.path.exists("coords.txt"):
        with open("coords.txt", "r") as file:
            coords = file.read().split(",")
            x, y = int(coords[0]), int(coords[1])
            original_coords.append(x)
            original_coords.append(y)

    # voice recognize
    data = stream.read(CHUNK)
    if vad.is_speech(data, RATE):
        print("is speech")
        decoder.process_raw(data, False, False)
        print(decoder.hyp())
    else:
        decoder.end_utt()
        decoder.start_utt()

    if decoder.hyp() is not None:
        hypothesis = decoder.hyp()
        # print(decoder.hyp())
        print('Recognized: "{}"'.format(hypothesis.hypstr))
        if hypothesis.hypstr == 'open':
            print('Detected keyword "open"')

            # locate the target light
            min_distance = float("inf")
            nearest_light = None
            for light in lights:
                distance = math.sqrt(
                    (light["pos"][0] - original_coords[0]) ** 2 + (light["pos"][1] - original_coords[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_light = light

            # turn on/off light
            for light in lights:
                light["on"] = False
            if nearest_light:
                nearest_light["on"] = True
                light_timer = time.time() + 2  # turn off the light after 2s

            decoder.end_utt()
            decoder.start_utt()

        else:
            print('Recognized "{}", expected "open"'.format(hypothesis.hypstr))
    # decoder.end_utt()
    # decoder.start_utt()

    if light_timer > 0 and time.time() > light_timer:
        for light in lights:
            light["on"] = False
        light_timer = 0

    screen.fill((255, 255, 255))

    # light
    for light in lights:
        if light["on"]:
            screen.blit(light_on, (light["pos"][0] - 25, light["pos"][1] - 25))
        else:
            screen.blit(light_off, (light["pos"][0] - 25, light["pos"][1] - 25))

    # receiver
    screen.blit(receiver, (original_coords[0], original_coords[1]))

    pygame.display.flip()

decoder.end_utt()

pygame.quit()
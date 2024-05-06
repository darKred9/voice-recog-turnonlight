# voice-recog-turnonlight
Turn on the nearest light based on the given coordinates. Triggered by voice.

Course project of 17-422/722,05-499/899, Spring 2024: Building User-Focused Sensing Systems

- `basic.py`: turn on the nearest light based on the coordinates given by `coords.txt`. work without voice recog.
- `recog_cmu`: work with CMU pocketsphinx model (low accuracy; low latency)
- `recog_vosk`: work with Vosk model. https://alphacephei.com/vosk/models `vosk-model-en-us-0.22` (high accuracy; high latency)

- simulated by pygame

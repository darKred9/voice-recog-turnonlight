# voice-recog-turnonlight
Turn on nearest light based onj give coordinates. Triggered by voice.

- `basic.py`: turn on the nearest light based on the coords given by `coords.txt`. work without voice recog.
- `recog_cmu`: work with cmu pocketsphinx model (low accuracy; low latency)
- `recog_vosk`: work with vosk model. https://alphacephei.com/vosk/models `vosk-model-en-us-0.22` (high accuracy; high latency)

- simulated by pygame

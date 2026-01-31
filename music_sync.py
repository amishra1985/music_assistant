import os
import random
import pyaudio
import numpy as np
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# Convert hue/saturation to RGB
def hs_to_rgb(h, s):
    s = s / 100
    h = h / 360
    i = int(h * 6)
    f = h * 6 - i
    p = int(255 * (1 - s))
    q = int(255 * (1 - f * s))
    t = int(255 * (1 - (1 - f) * s))
    i = i % 6
    if i == 0:
        return [255, t, p]
    if i == 1:
        return [q, 255, p]
    if i == 2:
        return [p, 255, t]
    if i == 3:
        return [p, q, 255]
    if i == 4:
        return [t, p, 255]
    if i == 5:
        return [255, p, q]


# Home Assistant Config
HA_URL = os.getenv("HA_URL", "http://localhost:8123/api/services/light/turn_on")
HA_TOKEN = os.getenv("HA_TOKEN", "")
LIGHTS = ["light.family_room_1", "light.family_room_2", "light.family_room_3",
          "light.kitchen_light_1", "light.kitchen_light_2", "light.kitchen_light_3"]

# Microphone settings
CHUNK = 4096       # larger chunk = smoother detection
RATE = 44100
THRESHOLD = 1000   # adjust based on your music volume
MIN_TIME_BETWEEN_BEATS = 0.15  # seconds between triggers

# Transition & brightness settings
TRANSITION = 0.1
MAX_BRIGHTNESS = 255

# -----------------------------------------

# Initialize PyAudio
p = pyaudio.PyAudio()

# List available audio devices to find your virtual cable
print("Available audio input devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info['name'])

device_index = 4 #int(input("Enter device index for virtual audio device: "))

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("Music-beat sync started! Play music through the virtual device...")

last_beat_time = 0

try:
    while True:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)

        # FFT to get frequency spectrum
        fft = np.fft.rfft(data)
        freq = np.fft.rfftfreq(len(data), 1/RATE)

        # Focus on bass (20-150 Hz)
        bass_indices = np.where((freq >= 20) & (freq <= 150))
        bass = np.abs(fft[bass_indices]).mean()

        current_time = time.time()
        print(f"bass:{bass}")
        if bass > THRESHOLD and (current_time - last_beat_time) > MIN_TIME_BETWEEN_BEATS:
            brightness = min(int(bass/10000), MAX_BRIGHTNESS)
            hue = random.randint(0, 360)  # random color
            saturation = 100
            rgb = hs_to_rgb(hue, saturation)

            payload = {
                "entity_id": LIGHTS,
                "brightness": brightness,
                "transition": TRANSITION,
                "rgb_color": rgb
            }
            headers = {
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json"
            }

            requests.post(HA_URL, json=payload, headers=headers)
            last_beat_time = current_time


        time.sleep(0.03)

except KeyboardInterrupt:
    print("Stopping music sync...")
    stream.stop_stream()
    stream.close()
    p.terminate()
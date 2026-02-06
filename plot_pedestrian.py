import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import numpy as np
import time

BACKGROUND_IMG = "images/background.png"
ICON1_A_IMG = "images/icon1a.png"
ICON1_B_IMG = "images/icon1b.png"
ICON2_IMG = "images/icon2.png"
TEXT1A_IMG = "images/text1a.png"
TEXT1B_IMG = "images/text1b.png"
TEXT2_IMG = "images/text2.png"

ICON_POS = (0.3, 0.20)
TEXT_POS = (0.5, 0.675)

ICON_SIZE = 0.15
TEXT_SIZE = 0.3

ANIM_START = 2
ANIM_END = 5
BLINK_START = 5
ICON_SWITCH = 8
DISAPPEAR_TIME = 10

TEXT_ICON_START = 3
TEXT_ICON_END = 9

ANIM_INTERVAL = 0.3   # seconds (flipbook animation)
BLINK_INTERVAL = 0.5
FPS = 20

# Setup Figure
fig, ax = plt.subplots()
ax.axis("off")

bg = mpimg.imread(BACKGROUND_IMG)
ax.imshow(bg)
ax.set_xlim(0, bg.shape[1])
ax.set_ylim(bg.shape[0], 0)

# Load & flip icons vertically
icon1a = np.flipud(mpimg.imread(ICON1_A_IMG))
icon1b = np.flipud(mpimg.imread(ICON1_B_IMG))
icon2 = np.flipud(mpimg.imread(ICON2_IMG))
text1a = np.flipud(mpimg.imread(TEXT1A_IMG))
text1b = np.flipud(mpimg.imread(TEXT1B_IMG))
text2 = np.flipud(mpimg.imread(TEXT2_IMG))

extent_main = [
    bg.shape[1] * (ICON_POS[0] - ICON_SIZE / 2),
    bg.shape[1] * (ICON_POS[0] + ICON_SIZE / 2),
    bg.shape[0] * (ICON_POS[1] - ICON_SIZE / 2),
    bg.shape[0] * (ICON_POS[1] + ICON_SIZE / 2),
]

extent_text = [
    bg.shape[1] * (TEXT_POS[0] - TEXT_SIZE / 2),
    bg.shape[1] * (TEXT_POS[0] + TEXT_SIZE / 2),
    bg.shape[0] * (TEXT_POS[1] - TEXT_SIZE / 2),
    bg.shape[0] * (TEXT_POS[1] + TEXT_SIZE / 2),
]

icon_artist = ax.imshow(icon1a, extent=extent_main, alpha=0.0)
text_artist = ax.imshow(text1a, extent=extent_text, alpha=0.0)

start_time = time.time()

# -----------------------
# Animation Logic
# -----------------------
def update(frame):
    elapsed = time.time() - start_time

    # --- Animated alternation (flipbook effect) ---
    if ANIM_START <= elapsed < ANIM_END:
        phase = int((elapsed - ANIM_START) / ANIM_INTERVAL) % 2
        icon_artist.set_data(icon1a if phase == 0 else icon1b)
        text_artist.set_data(text1a if phase == 0 else text1b)
        icon_artist.set_alpha(1.0)
        text_artist.set_alpha(1.0)

    # --- Blinking phase ---
    elif BLINK_START <= elapsed < ICON_SWITCH:
        icon_artist.set_data(icon2)
        text_artist.set_data(text2)
        blink = int((elapsed - BLINK_START) / BLINK_INTERVAL) % 2
        icon_artist.set_alpha(1.0 if blink == 0 else 0.0)
        text_artist.set_alpha(1.0 if blink == 0 else 0.0)

    # --- Final icon ---
    elif ICON_SWITCH <= elapsed < DISAPPEAR_TIME:
        icon_artist.set_data(icon2)
    else:
        icon_artist.set_alpha(0.0)
        text_artist.set_alpha(0.0)

    return icon_artist, text_artist

ani = FuncAnimation(fig, update, interval=1000 / FPS, blit=True)
plt.show()

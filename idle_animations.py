from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.color import AQUA, JADE
from adafruit_led_animation.animation.multicolor_comet import MulticolorComet
import adafruit_led_animation.color as color

import time
import board
import neopixel

TOTAL_PIXELS = 54
pixels = neopixel.NeoPixel(board.D5, TOTAL_PIXELS, brightness=1.0)

rainbow_sparkle_strip_1 = RainbowSparkle(pixels, speed=0.1, num_sparkles=10)
chase_strip_1 = Chase(pixels, speed=0.01, size=3, spacing=16, color=color.PURPLE)
comet_strip_1 = Comet(pixels, speed=0.002, color=color.JADE, tail_length=30, bounce=True)
rainbow_chase_strip_1 = RainbowChase(pixels, speed=0.05, size=5, spacing=3)
pulse_strip_1 = Pulse(pixels, speed=0.1, color=color.MAGENTA, period=2)
colorcycle = ColorCycle(pixels, 0.5)
multicolor_comet = MulticolorComet(pixels, speed=0.02,
                                   colors=[color.PINK, color.GOLD, color.RED, color.PURPLE, color.BLUE, color.AQUA,
                                           color.ORANGE, color.YELLOW, (227, 113, 240), (35, 245, 12)], tail_length=20,
                                   bounce=True)

sequence = AnimationSequence(chase_strip_1, multicolor_comet, comet_strip_1, rainbow_chase_strip_1,
                             rainbow_sparkle_strip_1, auto_clear=True)

last_checked = 0
interval = 20

# ! ----------------------
# ! idle animations
while True:
    now = time.monotonic()
    print(f"now: {now}, last check: {last_checked}")

    if now - last_checked > interval:
        last_checked = now
        sequence.next()

    # rainbow_sparkle_strip_1.animate()
    sequence.animate()

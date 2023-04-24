import pygame.mixer as pg_mix

pg_mix.init()


class SoundClass:
    def __init__(self, file):
        self.file = file
        self.pg_mix_sound = pg_mix.Sound(self.file)
        self.duration_ms = int(self.pg_mix_sound.get_length() * 1000)

    def play(self, loops=0):
        self.pg_mix_sound.play(loops=loops)


SOUNDS_DICT = {
    "universal_move": SoundClass("sounds/short_bubble.ogg"),
    "jelly": SoundClass("sounds/short_jelly.ogg"),
    "coin": SoundClass("sounds/short_coin.ogg"),
    "win": SoundClass("sounds/winfantasia2.ogg"),
    "draw": SoundClass("sounds/short_robot.ogg"),
    "loss": SoundClass("sounds/short_drum.ogg"),
    "start": SoundClass("sounds/short_woosh.ogg")
}


def stop_sounds():
    global SOUNDS_DICT
    for sound_object in SOUNDS_DICT.values():
        sound_object.pg_mix_sound.stop()

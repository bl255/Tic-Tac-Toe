from tkinter import Canvas
from images_theme import render_image_on_canvas
from PIL import Image
from importlib import import_module
import settings_gui as set_gui


class Player:
    def __init__(self, name, animation, sound, dict_call=0):
        self.name = name
        self.taken = []
        self.animation = animation
        self.dict_call = dict_call
        self.sound = sound

    def adjust_theme(self, theme_settings):
        self.name, self.animation, self.sound = theme_settings


class GameCell:
    def __init__(self, index, top_left):
        self.cell_is_free = True
        self.click_coordinates = (0, 0)
        self.index = index
        self.top_left = top_left
        self.animation = None


class Theme:
    def __init__(self, main_canvas, win_animation, draw_animation, canvas_background_graphics,
                 settings_module, player_1_settings, player_2_settings, reset_actions=lambda: None):
        self.main_canvas = main_canvas
        self.win_animation = win_animation
        self.draw_animation = draw_animation
        self.canvas_background_graphics = canvas_background_graphics

        self.player_1_settings = player_1_settings
        self.player_2_settings = player_2_settings

        self.settings_module = settings_module
        self.main_text_kwargs = self.load_from_settings_file("main_text_kwargs")
        self.btn_kwargs = self.load_from_settings_file("btn_kwargs")
        self.btn_images = self.load_from_settings_file("btn_images")

        self.reset_actions = reset_actions

    def configure_main_canvas(self):
        self.main_canvas()

    def draw_background_graphics(self):
        self.canvas_background_graphics()

    def reset_actions(self):
        self.reset_actions()

    def win_animation(self):
        self.win_animation()

    def draw_animation(self):
        self.draw_animation()

    def player_1_animation(self, player_1_animation_args):
        self.player_1_animation(*player_1_animation_args)

    def player_2_animation(self, player_2_animation_args):
        self.player_2_animation(*player_2_animation_args)

    def load_from_settings_file(self, item):
        module = import_module(self.settings_module)
        return getattr(module, item)


class UserCanvasButton(Canvas):
    def __init__(self, main_canvas, top_left, text, img_key="button", function=None, rule=None, img_file=None,
                 main_canvas_tags="btn_canvas", **kwargs):
        super(UserCanvasButton, self).__init__()
        self.main_canvas = main_canvas
        self.function = function
        self.highlightthickness = 0
        self.text = text
        self.bg = kwargs["btn_bg"]
        self.fg = kwargs["btn_fg"]
        self.strike_off = kwargs["btn_strike_off"]
        self.font = kwargs["btn_font"]
        self.btn_size = set_gui.btn_size
        self.width, self.height = self.btn_size
        self.img_file = img_file
        self.img_key = img_key
        self.rule = rule
        self.configure(width=self.width, height=self.height, bg=self.bg, highlightthickness=self.highlightthickness)
        self.main_canvas.create_window(*top_left, window=self, tags=main_canvas_tags)
        self.bind("<Button-1>", self.on_click)
        if img_file is not None:
            with Image.open(self.img_file) as img_file:
                img = img_file.resize(self.btn_size)
                render_image_on_canvas(self, dict_key=self.img_key, pil_image=img,
                                       additional_tags=("button", self.img_key))
        self.create_text(self.width // 2, self.height // 2, text=self.text, fill=self.fg, font=self.font)
        self.strike_line = self.create_line(0 + self.strike_off, self.height // 2, self.width - self.strike_off,
                                            self.height // 2, fill=self.fg, width=2, tags="strikeline")
        self.itemconfig(self.strike_line, state="hidden")
        self.striketrough()

    def on_click(self, event):
        self.function()
        self.striketrough()

    def striketrough(self):
        if self.rule is not None:
            if not self.rule:
                self.itemconfig(self.strike_line, state="normal")
            else:
                self.itemconfig(self.strike_line, state="hidden")

    def find_tag(self, tag):
        self.find_withtag(tag)
                
    def adjust_theme(self, img_file=None, **theme_settings):
        self.delete("all")
        self.bg = theme_settings["btn_bg"]
        self.fg = theme_settings["btn_fg"]
        self.strike_off = theme_settings["btn_strike_off"]
        self.font = theme_settings["btn_font"]
        self.img_file = img_file

        if self.img_file is not None:
            with Image.open(self.img_file).resize(self.btn_size) as img_file:
                img = img_file.resize(self.btn_size)
                render_image_on_canvas(self, dict_key=self.img_key, pil_image=img,
                                       additional_tags=("button", self.img_key))
        self.create_text(self.width // 2, self.height // 2, text=self.text, fill=self.fg, font=self.font)
        self.strike_line = self.create_line(0 + self.strike_off, self.height // 2, self.width - self.strike_off,
                                            self.height // 2, fill=self.fg, width=2, tags="strikeline")
        self.itemconfig(self.strike_line, state="hidden")
        self.striketrough()


class MainText:
    def __init__(self, canvas, text, pos, **kwargs):
        self.canvas = canvas
        self.width = set_gui.text_width
        self.font = kwargs["font"]
        self.color = kwargs["color"]
        self.pos = pos
        self.text = text

    def render_text(self, new_text):
        self.canvas.delete("main_text_tag")
        self.canvas.create_text(*self.pos, text=new_text, width=self.width, fill=self.color, font=self.font,
                                tag="main_text_tag", justify="center")

    def adjust_theme(self, **theme_settings):
        self.font = theme_settings["font"]
        self.color = theme_settings["color"]

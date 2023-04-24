from PIL import Image, ImageTk
import os
import random
from vector_theme import text_outline
import settings_images_theme as set_imt
import settings_gui as set_gui

IMAGE_CONTAINER = {}
TK_IMAGE_CONTAINER = {}
CANVAS_IMAGE_CONTAINER = {}
PLAY_IMAGE_OPTIONS = {}


def configure_main_canvas(canvas, bg=set_imt.canvas_background):
    canvas.configure(bg=bg, highlightthickness=0)


def canvas_background_graphics(canvas, grid_top_left, cell_size):
    configure_main_canvas(canvas, bg=set_imt.canvas_background)
    canvas_image(canvas)
    draw_grid(canvas, grid_top_left, cell_size)
    text_image(canvas)
    text_outline(canvas, tags="images_theme", outline=set_imt.main_text_outline_color)


def render_image_on_canvas(canvas, dict_key, pil_image: Image.Image, x=0, y=0,
                           additional_tags=()):
    global IMAGE_CONTAINER, TK_IMAGE_CONTAINER
    IMAGE_CONTAINER[dict_key] = pil_image
    TK_IMAGE_CONTAINER[dict_key] = ImageTk.PhotoImage(IMAGE_CONTAINER[dict_key])
    if canvas.winfo_id() not in CANVAS_IMAGE_CONTAINER:
        CANVAS_IMAGE_CONTAINER[canvas.winfo_id()] = {}
    CANVAS_IMAGE_CONTAINER[canvas.winfo_id()][dict_key] = canvas.create_image(
        x, y, image=TK_IMAGE_CONTAINER[dict_key], anchor="nw", tags=("images_theme",
                                                                     *additional_tags))


def player1(canvas, cell_size, cell_id=0, size=set_imt.player_image_size, click_x=0, click_y=0, cell_top_left=(0, 0),
            dir_path=set_imt.image_path_pl_1, beyond_border=10, img_scale=None, global_list="1"):
    global PLAY_IMAGE_OPTIONS
    if global_list not in PLAY_IMAGE_OPTIONS:
        PLAY_IMAGE_OPTIONS[global_list] = os.listdir(dir_path)
    if len(PLAY_IMAGE_OPTIONS[global_list]) > 0:
        img = PLAY_IMAGE_OPTIONS[global_list].pop(random.randint(0, len(PLAY_IMAGE_OPTIONS[global_list]) - 1))
    else:
        img = random.choice(os.listdir(dir_path))
    file = f"{dir_path}/{img}"
    with Image.open(file) as opened:
        opened_width, opened_height = opened.size
        if img_scale is None:
            img_scale = size / max(opened_width, opened_height)
        image_width, image_height = int(opened_width * img_scale), int(opened_height * img_scale)
        put_x, put_y = click_x - image_width // 2, click_y - image_height // 2
        min_x, min_y = cell_top_left[0] - beyond_border, cell_top_left[1] - beyond_border
        max_x = cell_top_left[0] + cell_size + beyond_border - image_width
        max_y = cell_top_left[1] + cell_size + beyond_border - image_height

        put_x = min_x if put_x < min_x else max_x if put_x > max_x else put_x
        put_y = min_y if put_y < min_y else max_y if put_y > max_y else put_y

        resized = opened.resize((image_width, image_height))
        render_image_on_canvas(canvas, cell_id, resized, x=put_x, y=put_y,
                               additional_tags=["played_game", "player", f"{cell_id}"])


def player2(canvas, cell_size, dir_path=set_imt.image_path_pl_2, **kwargs):
    player1(canvas=canvas, cell_size=cell_size, dir_path=dir_path, global_list="2", **kwargs)


def draw_grid(canvas, top_left, cell_size, line_color=set_imt.clr_grid,
              line_width=set_imt.grid_linewidth, tags="images_theme", add=40):
    with Image.open(set_imt.image_path_grid_background) as img_file:
        img = img_file.resize((3 * cell_size + add, 3 * cell_size + add))
        render_image_on_canvas(canvas, "grid", img, x=top_left[0] - 20, y=top_left[1] - 20)

    start_x, start_y = top_left

    for num in range(1, 3):
        # vertical lines
        canvas.create_line(start_x + cell_size * num, start_y,
                           start_x + cell_size * num, start_y + cell_size * 3,
                           fill=line_color, width=line_width, arrow=None, tags=tags)
        # horizontal lines
        canvas.create_line(start_x, start_y + cell_size * num,
                           start_x + cell_size * 3, start_y + cell_size * num,
                           fill=line_color, width=line_width, arrow=None, tags=tags)


def text_image(canvas, outline_size=set_gui.text_outline_size, text_pos=(400, 450), over=10):
    outline_width, outline_height = outline_size
    img_x, img_y = text_pos[0] - (outline_width//2 + over),  text_pos[1] - (outline_height//2 + over)
    with Image.open(set_imt.image_path_text_background) as img_file:
        img = img_file.resize((outline_width + 2 * over, outline_height + 2 * over))
        render_image_on_canvas(canvas, "text", img, x=img_x, y=img_y)


def canvas_image(canvas, img_width=set_imt.canvas_img_width, img_height=set_imt.canvas_img_height):
    with Image.open(set_imt.image_path_canvas_background) as img_file:
        img = img_file.resize((img_width, img_height))
        render_image_on_canvas(canvas, "background", img)


def images_to_greyscale(canvas, dict_key_filter=lambda key: True):
    global IMAGE_CONTAINER, TK_IMAGE_CONTAINER, CANVAS_IMAGE_CONTAINER

    def image_to_greyscale(im_canvas, img_dict_key):
        IMAGE_CONTAINER[f"gs_{img_dict_key}"] = IMAGE_CONTAINER[img_dict_key].convert("LA").convert("RGBA")
        TK_IMAGE_CONTAINER[img_dict_key] = ImageTk.PhotoImage(IMAGE_CONTAINER[f"gs_{img_dict_key}"])
        im_canvas.itemconfig(CANVAS_IMAGE_CONTAINER[im_canvas.winfo_id()][img_dict_key],
                             image=TK_IMAGE_CONTAINER[img_dict_key])

    for canvas_id in CANVAS_IMAGE_CONTAINER.keys():
        for dict_key in CANVAS_IMAGE_CONTAINER[canvas_id].keys():
            if dict_key_filter(dict_key):
                if canvas.winfo_id() == canvas_id:
                    image_to_greyscale(canvas, dict_key)


def win_animation(canvas, winning_cells, buttons):
    images_to_greyscale(canvas, dict_key_filter=lambda x: x not in winning_cells)
    for button in buttons:
        images_to_greyscale(button)


def draw_animation(canvas, buttons):
    images_to_greyscale(canvas)
    for button in buttons:
        images_to_greyscale(button)


def reset_actions(canvas, buttons):
    global PLAY_IMAGE_OPTIONS
    PLAY_IMAGE_OPTIONS = {}
    global TK_IMAGE_CONTAINER, IMAGE_CONTAINER
    for item in ["background", "text", "grid"]:
        TK_IMAGE_CONTAINER[item] = ImageTk.PhotoImage(IMAGE_CONTAINER[item])
        canvas.itemconfig(CANVAS_IMAGE_CONTAINER[canvas.winfo_id()][item],
                          image=TK_IMAGE_CONTAINER[item])

    for button in buttons:
        for item in CANVAS_IMAGE_CONTAINER[button.winfo_id()]:
            TK_IMAGE_CONTAINER[item] = ImageTk.PhotoImage(IMAGE_CONTAINER[item])
            button.itemconfig(CANVAS_IMAGE_CONTAINER[button.winfo_id()][item],
                              image=TK_IMAGE_CONTAINER[item])

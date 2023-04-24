import settings_vector_theme as set_vt
import settings_gui as set_gui


def canvas_background_graphics(canvas, grid_top_left, cell_size):
    configure_main_canvas(canvas)
    round_rectangle(canvas)
    draw_grid(canvas, grid_top_left, cell_size)
    text_outline(canvas)


def configure_main_canvas(canvas, bg=set_vt.canvas_background):
    canvas.configure(bg=bg, highlightthickness=0)


def player1(canvas, cell_size, cl=set_vt.clr_player_1, cell_top_left=(0, 0), off=16, line_width=3,
            click_x=None, click_y=None, cell_id=None, dash=None, additional_tags=()):
    canvas.create_line(cell_top_left[0] + off, cell_top_left[1] + off, cell_top_left[0] + cell_size - off,
                       cell_top_left[1] + cell_size - off,
                       fill=cl, width=line_width, dash=dash,
                       tags=("vector_theme", "played_game", "player", f"{cell_id}", *additional_tags))
    canvas.create_line(cell_top_left[0] + off, cell_top_left[1] + cell_size - off, cell_top_left[0] + cell_size - off,
                       cell_top_left[1] + off,
                       fill=cl, width=line_width, dash=dash,
                       tags=("vector_theme", "played_game", "player", f"{cell_id}", *additional_tags))


def player2(canvas, cell_size, cl=set_vt.clr_player_2, cell_top_left=(0, 0), off=20, line_width=3,
            click_x=None, click_y=None, cell_id=None, dash=None, additional_tags=()):
    canvas.create_oval(cell_top_left[0] + off, cell_top_left[1] + off, cell_top_left[0] + cell_size - off,
                       cell_top_left[1] + cell_size - off,
                       outline=cl, width=line_width, dash=dash,
                       tags=("vector_theme", "played_game", "player", f"{cell_id}", *additional_tags))


def draw_grid(canvas, top_left, cell_size, line_color=set_vt.clr_grid,
              line_width=set_vt.grid_linewidth, tags="vector_theme"):
    start_x, start_y = top_left
    shift = 0
    for local_width in [line_width, line_width // 2, line_width // 4]:
        for num in range(1, 3):
            # vertical lines
            canvas.create_line(start_x + cell_size * num, start_y - shift,
                               start_x + cell_size * num, start_y + cell_size * 3 + shift,
                               fill=line_color, width=local_width, tags=tags)
            # horizontal lines
            canvas.create_line(start_x - shift, start_y + cell_size * num,
                               start_x + cell_size * 3 + shift, start_y + cell_size * num,
                               fill=line_color, width=local_width, tags=tags)
        shift += 4


def text_outline(canvas, tags="vector_theme", outline=set_vt.main_text_outline_clr, text_pos=set_gui.text_pos,
                 outline_size=set_gui.text_outline_size):
    width, height = outline_size
    canvas.create_rectangle(text_pos[0] - width // 2, text_pos[1] - height // 2,
                            text_pos[0] + width // 2, text_pos[1] + height // 2,
                            outline=outline, dash=1, width=2, tags=tags)


def round_rectangle(canvas, r=set_vt.canvas_rounding_radius, bg=set_vt.window_background_clr,
                    fg=set_vt.canvas_background):
    max_x, max_y = int(canvas["width"]), int(canvas["height"])

    def get_points(k):
        return ((0, 0, 0 + k, 0 + k),
                (max_x, 0, max_x - k, 0 + k),
                (max_x, max_y, max_x - k, max_y - k),
                (0, max_y, 0 + k, max_y - k))

    for pos1 in get_points(r // 2):
        canvas.create_rectangle(*pos1, fill=bg, width=0, tags="vector_theme")
    for pos2 in get_points(r):
        canvas.create_oval(*pos2, fill=fg, width=0, tags="vector_theme")


def win_animation(canvas, active_player, grid_top_left, cell_size, cells, winning_cells, cl="white",
                  win_cl=set_vt.canvas_background, buttons=None):
    for cell_index in winning_cells:
        x1, y1 = cells[cell_index].top_left[0], cells[cell_index].top_left[1]
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill=cl, width=0, tags=("vector_theme", "played_game", "win"))
        active_player.animation({
            "cl": win_cl, "cell_top_left": cells[cell_index].top_left, "line_width": 6})
    draw_grid(canvas, grid_top_left, cell_size)


def draw_animation(canvas):
    shapes_ids = [shape_id for shape_id in canvas.find_all() if
                  set(canvas.gettags(shape_id)) >= {"vector_theme", "player"}]
    for canvas_id in shapes_ids:
        canvas.itemconfig(canvas_id, width=1, dash=1)

from tic_tac_toe_subclasses import UserCanvasButton, MainText, Theme, Player, GameCell
import instructions_texts as i_txt
from game_logic import autoplay, winning_cells, is_draw
from sound import SOUNDS_DICT, stop_sounds
import vector_theme as vt
import images_theme as imt
import settings_gui as set_gui

RESUL_SOUND_DELAY_MS = 0
START_SOUND_DELAY_MS = 200
ANIMATION_PART_TIME_MS = 100


class TicTacToe:
    def __init__(self, canvas, grid_top_left=set_gui.grid_top_left, cell_size=set_gui.grid_cell_size):
        self.canvas = canvas
        self.grid_top_left = grid_top_left
        self.cell_size = cell_size
        self.multiplayer = False
        self.sound = True
        self.players = None
        self.active_player = None
        self.images_theme_on = True

        self.shown_text = None
        self.result = None
        self.active_cell_index = None
        self.cells = None
        self.game_is_on = None
        self.timer = None
        self.winning_cells = set()
        self.turn_timeline = None
        self.after_actions = []

        self.main_text = None
        self.reset_button = None
        self.playmode_button = None
        self.sound_button = None
        self.theme_button = None

        self.themes = {"vector_theme":
                       Theme(lambda: vt.configure_main_canvas(self.canvas),
                             lambda: vt.win_animation(
                                 self.canvas, self.active_player, self.grid_top_left, self.cell_size, self.cells,
                                 self.winning_cells),
                             lambda: vt.draw_animation(self.canvas),
                             lambda: vt.canvas_background_graphics(
                                 self.canvas, self.grid_top_left, self.cell_size),
                             "settings_vector_theme",
                             ("x", lambda kwargs: vt.player1(self.canvas, self.cell_size, **kwargs),
                              SOUNDS_DICT["universal_move"]),
                             ("O", lambda kwargs: vt.player2(self.canvas, self.cell_size, **kwargs),
                              SOUNDS_DICT["universal_move"])),

                       "images_theme":
                           Theme(lambda: imt.configure_main_canvas(self.canvas),
                                 lambda: imt.win_animation(self.canvas, self.winning_cells, self.all_buttons),
                                 lambda: imt.draw_animation(self.canvas, self.all_buttons),
                                 lambda: imt.canvas_background_graphics(self.canvas, self.grid_top_left,
                                                                        self.cell_size),
                                 "settings_images_theme",
                                 ("coin", lambda kwargs: imt.player1(self.canvas, self.cell_size, **kwargs),
                                  SOUNDS_DICT["coin"]),
                                 ("bear", lambda kwargs: imt.player2(self.canvas, self.cell_size, **kwargs),
                                  SOUNDS_DICT["jelly"]),
                                 lambda: imt.reset_actions(self.canvas, self.all_buttons)),
                       }
        self.current_theme = self.themes[list(self.themes.keys())[int(self.images_theme_on)]]
        self.set_players()
        self.set_new_game()

        self.graphic_elements()
        self.shown_text = i_txt.whole_text.format(
            self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer], i_txt.width, i_txt.start_text)
        self.main_text.render_text(self.shown_text)
        self.canvas.bind("<Button-1>", self.click_on_cell)

    @property
    def all_buttons(self):
        return self.reset_button, self.playmode_button, self.sound_button, self.theme_button

    @property
    def cells_top_lefts(self):
        cells_top_lefts = []
        start_x, start_y = self.grid_top_left
        for k1 in range(3):
            for k2 in range(3):
                cells_top_lefts.append((start_x + self.cell_size * k2, start_y + self.cell_size * k1))
        return cells_top_lefts

    @property
    def free_cells(self):
        return [c.index for c in self.cells if c.cell_is_free]

    def click_on_cell(self, event):
        if self.game_is_on:
            x, y = self.get_click_coordinates(event)
            self.active_cell_index = self.get_clicked_cell_index(x, y)
            if self.active_cell_index is not None and self.cells[self.active_cell_index].cell_is_free:

                self.game_is_on = False
                self.cells[self.active_cell_index].click_coordinates = x, y
                self.turn_timeline = 0
                self.cells[self.active_cell_index].cell_is_free = False
                self.active_player.taken.append(self.active_cell_index)
                self.player_animation_sound_block()
                self.winning_draw_actions()

                if self.result is None:
                    if not self.multiplayer:

                        self.autoplay_block()
                        self.wait_animation()
                        self.custom_after(self.after_main_text_block)
                        self.custom_after(self.after_animation_sound_block)

                    else:
                        self.active_player = self.players[not self.active_player.dict_call]
                        self.shown_text = i_txt.whole_text.format(
                            self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer], i_txt.width, "")
                        self.main_text.render_text(self.shown_text)
                        self.game_is_on = True

    def autoplay_block(self, event=None):
        opponent_taken = self.active_player.taken
        self.active_player = self.players[not self.active_player.dict_call]
        taken = self.active_player.taken
        self.active_cell_index = autoplay(self.free_cells, taken, opponent_taken)
        self.cells[self.active_cell_index].click_coordinates = \
            (self.cells[self.active_cell_index].top_left[0] + self.cell_size // 2,
             self.cells[self.active_cell_index].top_left[1] + self.cell_size // 2)
        self.cells[self.active_cell_index].cell_is_free = False
        self.active_player.taken.append(self.active_cell_index)

    def player_animation_sound_block(self):
        self.active_player.animation({"cell_id": self.active_cell_index,
                                      "cell_top_left": self.cells[self.active_cell_index].top_left,
                                      "click_x": self.cells[self.active_cell_index].click_coordinates[0],
                                      "click_y": self.cells[self.active_cell_index].click_coordinates[1]})
        if self.sound:
            self.active_player.sound.play()
            self.turn_timeline += self.active_player.sound.duration_ms

    def winning_draw_actions(self):
        winning = winning_cells(self.active_player.taken)

        if winning:
            self.winning_cells = winning
            self.shown_text = i_txt.whole_text.format("", i_txt.width, "", i_txt.width,
                                                      i_txt.win_text.format(self.active_player.name))
            self.main_text.render_text(self.shown_text)
            self.result = self.active_player.name
            self.current_theme.win_animation()
            if self.sound:
                self.custom_after(SOUNDS_DICT["win"].play, add_time=RESUL_SOUND_DELAY_MS)

        elif is_draw(self.active_player.taken):
            self.shown_text = i_txt.whole_text.format("", i_txt.width, "", i_txt.width, i_txt.draw_text)
            self.main_text.render_text(self.shown_text)
            self.result = "draw"
            self.current_theme.draw_animation()
            if self.sound:
                self.custom_after(SOUNDS_DICT["draw"].play, add_time=RESUL_SOUND_DELAY_MS)

    def after_main_text_block(self):
        self.player_animation_sound_block()
        self.shown_text = i_txt.whole_text.format(
            self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer], i_txt.width,
            "")
        self.main_text.render_text(self.shown_text)

    def after_animation_sound_block(self):
        self.winning_draw_actions()
        if self.result is None:
            self.active_player = self.players[not self.active_player.dict_call]
            self.shown_text = i_txt.whole_text.format(
                self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer],
                i_txt.width, "")
            self.main_text.render_text(self.shown_text)
            self.game_is_on = True

    def create_cells(self):
        cell_list = []
        for num, pos in enumerate(self.cells_top_lefts):
            cell = GameCell(index=num, top_left=pos)
            cell_list.append(cell)
        return cell_list

    def get_clicked_cell_index(self, x, y):
        if x is not None and y is not None:
            lim_x, lim_y = self.grid_top_left
            index = (x - lim_x) // self.cell_size + 3 * ((y - lim_y) // self.cell_size)
            return index

    def get_click_coordinates(self, event):
        lim_x, lim_y = self.grid_top_left
        x, y = event.x, event.y
        if lim_x <= x <= lim_x + 3 * self.cell_size and lim_y <= y <= lim_y + 3 * self.cell_size:
            return x, y
        return None, None

    def set_new_game(self):
        self.cells = self.create_cells()
        self.active_cell_index = 0
        self.turn_timeline = 0
        if self.sound:
            self.custom_after(SOUNDS_DICT["start"].play, add_time=START_SOUND_DELAY_MS)
            self.turn_timeline += SOUNDS_DICT["start"].duration_ms
        self.custom_after(self.game_on, add_time=START_SOUND_DELAY_MS)

    def set_players(self):
        self.players = (Player(*self.current_theme.player_1_settings),
                        Player(*self.current_theme.player_2_settings, dict_call=1))
        self.active_player = self.players[0]

    def reset(self):
        stop_sounds()
        self.cancel_after_actions()
        self.canvas.delete("played_game")
        self.current_theme.reset_actions()
        self.set_new_game()
        self.set_players()
        self.result = None
        self.winning_cells = set()
        self.turn_timeline = 0
        self.shown_text = i_txt.whole_text.format(
            self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer], i_txt.width, "")
        self.main_text.render_text(self.shown_text)

    def graphic_elements(self):
        self.current_theme.draw_background_graphics()

        self.main_text = MainText(self.canvas, self.shown_text, set_gui.text_pos, **self.current_theme.main_text_kwargs)
        self.reset_button = UserCanvasButton(self.canvas, set_gui.btn_poss[0], "RESET", function=self.reset,
                                             img_file=self.current_theme.btn_images[0], img_key="reset",
                                             **self.current_theme.btn_kwargs)
        self.playmode_button = UserCanvasButton(self.canvas, set_gui.btn_poss[1], "MULTIPLAYER",
                                                function=self.switch_playmode, rule=self.multiplayer,
                                                img_file=self.current_theme.btn_images[1], img_key="playmode",
                                                **self.current_theme.btn_kwargs)
        self.sound_button = UserCanvasButton(self.canvas, set_gui.btn_poss[2], "SOUND",
                                             function=self.switch_sound, rule=self.sound,
                                             img_file=self.current_theme.btn_images[2], img_key="sound",
                                             **self.current_theme.btn_kwargs)
        self.theme_button = UserCanvasButton(self.canvas, set_gui.btn_poss[3], "IMAGES",
                                             function=self.switch_theme,
                                             rule=self.images_theme_on,
                                             img_file=self.current_theme.btn_images[3], img_key="theme",
                                             **self.current_theme.btn_kwargs)

    def switch_playmode(self):
        self.active_player = self.players[not self.active_player]
        self.multiplayer = not self.multiplayer
        self.playmode_button.rule = self.multiplayer
        if all([self.result is None, not self.multiplayer, len(self.free_cells) == 9]):
            self.game_is_on = False
            self.autoplay_block()
            self.wait_animation()
            self.custom_after(self.after_main_text_block)
            self.custom_after(self.after_animation_sound_block)
            self.custom_after(self.game_on)

    def switch_sound(self):
        self.sound = not self.sound
        self.sound_button.rule = self.sound
        if not self.sound:
            stop_sounds()

    def switch_theme(self):
        self.images_theme_on = not self.images_theme_on
        theme_name = list(self.themes.keys())[int(self.images_theme_on)]
        self.current_theme = self.themes[theme_name]
        self.theme_button.rule = self.images_theme_on
        self.adjust_themed_elements()
        self.current_theme.configure_main_canvas()

        def handle_theme(shown_theme_tag, hidden_theme_tag):
            items = {shown_theme_tag: self.canvas.find_withtag(shown_theme_tag),
                     hidden_theme_tag: self.canvas.find_withtag(hidden_theme_tag)}
            self.canvas.itemconfig(hidden_theme_tag, state="hidden")
            if not items[shown_theme_tag]:
                self.current_theme.canvas_background_graphics()
            self.canvas.itemconfig(shown_theme_tag, state="normal")

            for player in self.players:
                for cell in player.taken:
                    if not [shape_id for shape_id in self.canvas.find_all() if
                            set(self.canvas.gettags(shape_id)) >= {shown_theme_tag, f"{cell}"}]:
                        player.animation({"cell_id": cell,
                                          "cell_top_left": self.cells[cell].top_left,
                                          "click_x": self.cells[cell].click_coordinates[0],
                                          "click_y": self.cells[cell].click_coordinates[1]})
            if self.result == "draw":
                self.current_theme.draw_animation()
                self.shown_text = i_txt.whole_text.format("", i_txt.width, "", i_txt.width, i_txt.draw_text)
            elif self.result is not None:
                self.current_theme.win_animation()
                self.shown_text = i_txt.whole_text.format(
                    "", i_txt.width, "", i_txt.width, i_txt.win_text.format(self.active_player.name))
            else:
                self.shown_text = i_txt.whole_text.format(
                    self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer], i_txt.width, "")

        if self.images_theme_on:
            handle_theme("images_theme", "vector_theme")
        if not self.images_theme_on:
            handle_theme("vector_theme", "images_theme")

        self.main_text.render_text(self.shown_text)

    def game_on(self):
        self.game_is_on = True

    def adjust_themed_elements(self):
        self.players[0].adjust_theme(self.current_theme.player_1_settings)
        self.players[1].adjust_theme(self.current_theme.player_2_settings)
        self.main_text.adjust_theme(**self.current_theme.main_text_kwargs)

        for num, button in enumerate(self.all_buttons):
            button.adjust_theme(img_file=self.current_theme.btn_images[num], **self.current_theme.btn_kwargs)

    def wait_animation(self):
        global ANIMATION_PART_TIME_MS
        hyphen_counts = (1, 3, 5, 7, 5, 3, 1)
        for num, hyphen_count in enumerate(hyphen_counts):
            text = i_txt.whole_text.format(self.active_player.name, i_txt.width, i_txt.mode_dict[self.multiplayer],
                                           i_txt.width, f"{'-' * hyphen_count}")
            self.custom_after(self.main_text.render_text, ANIMATION_PART_TIME_MS * num,  text)
        self.turn_timeline += (len(hyphen_counts) + 1) * ANIMATION_PART_TIME_MS

    def custom_after(self, function, add_time=0, *args):
        self.after_actions.append(self.canvas.after(self.turn_timeline + add_time, function, *args))

    def cancel_after_actions(self):
        for action in self.after_actions:
            self.canvas.after_cancel(action)
        self.after_actions = []

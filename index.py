import copy
import curses
import time
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
from random import choice

WIDTH = 40
HEIGHT = 25
TIMEOUT = 100


GAME_ELEMENTS = {
    "i": [[1], [1], [1], [1]],
    "j": [[1, 0, 0], [1, 1, 1]],
    "l": [[0, 0, 1], [1, 1, 1]],
    "o": [[1, 1], [1, 1]],
    "s": [[0, 1, 1], [1, 1, 0]],
    "t": [[0, 1, 0], [1, 1, 1]],
    "z": [[1, 1, 0], [0, 1, 1]]
}

BLOCK_COLORS = {
    "i": 1,
    "j": 2,
    "l": 3,
    "o": 4,
    "s": 5,
    "t": 6,
    "z": 4
}

TEXT_COLORS = {
    "black": u"\u001b[30;1m",
    "red": u"\u001b[31;1m",
    "green": u"\u001b[32;1m",
    "yellow": u"\u001b[33;1m",
    "blue": u"\u001b[34;1m",
    "magenta": u"\u001b[35c;1m",
    "cyan": u"\u001b[36;1m",
    "white": u"\u001b[37;1m",
    "reset": u"\u001b[0m"
}


class GameElement:

    def __init__(self, symbol, silhouette, pos_y, pos_x):
        self.symbol = symbol
        self.silhouette = silhouette
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_x_history = pos_x
        self.pos_y_history = pos_y

    @classmethod
    def generate_figure(cls, y, x):
        silhouettes = list(GAME_ELEMENTS.keys())
        figure = choice(silhouettes)
        return cls(figure, GAME_ELEMENTS[figure], y, x)


    def move_right(self, board_width):
        if self.pos_x + self.width() <= board_width - 1:
            self.pos_x_history = self.pos_x
            self.pos_x += 1

    def move_left(self):
        if self.pos_x > 0:
            self.pos_x_history = self.pos_x
            self.pos_x -= 1

    def move_down(self, board_hight):
        if self.pos_y + len(self.silhouette) <= board_hight - 1:
            self.pos_y_history = self.pos_y
            self.pos_y += 1

    def set_down(self):
        self.pos_y_history = self.pos_y
        self.pos_y += 1

    def reset_position(self):
        self.pos_x = self.pos_x_history

    def rotate(self, board_width, board_hight):
        list_of_tuples = zip(*self.silhouette[::-1])
        rotated_silhouette = [list(elem) for elem in list_of_tuples]
        new_max_width = len(max(rotated_silhouette, key=len))
        if self.pos_x + new_max_width <= board_width:
            self.silhouette = rotated_silhouette

    def height(self):
        return len(self.silhouette)

    def width(self):
        return len(max(self.silhouette, key=len))

    def __len__(self):
        return sum([sum(i) for i in self.silhouette])


class Board:

    def __init__(self, height=20, width=10):
        self.height = 20
        self.width = 10
        self._field = []

    def generate_board(self):
        self._field = [["x" for y in range(self.width)] for i in range(self.height)]
        return self._field

    def _line_done(self, line):
        return all([c != "x" for c in line])

    def check_matches(self):
        new_board = [i for i in self._field if not self._line_done(i)]
        lines_removed = self.height - len(new_board)
        for i in range(lines_removed):
            new_board.insert(0, ["x" for y in range(self.width)])
        self.update_board(new_board)
        return lines_removed

    def merge_map(self, element):
        field = copy.deepcopy(self._field)
        if element.pos_y + len(element.silhouette) <= len(field):
            for row, i in enumerate(element.silhouette):
                for column, y in enumerate(i):
                    if y == 1:
                        pos_y_row = element.pos_y + row
                        pos_x_column = element.pos_x + column
                        if len(field[pos_y_row]) >= pos_x_column:
                            field[pos_y_row][pos_x_column] = element.symbol
            return field

    def update_board(self, board_field):
        for e, i in enumerate(board_field):
            self._field[e] = i
        return self._field


class Render:

    def __init__(self, window):
        self.window = window

    def draw_next_element(self, element):
        for row in range(8):
            for col in range(8):
                self.window.addstr(row + 3, col + 25, " ", curses.color_pair(0))
        self.window.addstr(1, 24, "NEXT FIGURE:")
        color_number = BLOCK_COLORS.get(element.symbol)
        for num, row in enumerate(element.silhouette):
            increment = 1
            for cnum, column in enumerate(row):
                if column:
                    self.window.addstr(num + 3, cnum + 25 + increment, "X", curses.color_pair(color_number))
                    increment += 1
                    self.window.addstr(num + 3, cnum + 25 + increment, "X", curses.color_pair(color_number))
                else:
                    self.window.addstr(num + 3, cnum + 25 + increment, ".", curses.color_pair(8))
                    increment += 1
                    self.window.addstr(num + 3, cnum + 25 + increment, ".", curses.color_pair(8))
            increment = 0

    def draw_board(self, board):
        self.window.addstr(1, 5, "YOUR GAME BOARD")
        for num, row in enumerate(board):
            increment = 1
            for cnum, column in enumerate(row):
                color_number = BLOCK_COLORS.get(column)
                if color_number:
                    self.window.addstr(num + 3, cnum + 1 + increment, "X", curses.color_pair(color_number))
                    increment += 1
                    self.window.addstr(num + 3, cnum + 1 + increment, "X", curses.color_pair(color_number))
                else:
                    self.window.addstr(num + 3, cnum + 1 + increment, ".", curses.color_pair(7))
                    increment += 1
                    self.window.addstr(num + 3, cnum + 1 + increment, ".", curses.color_pair(7))
            increment = 0

    def draw_score(self, score, round):
        self.window.addstr(8, 24, "ROUND: %s" % round, curses.color_pair(0))
        self.window.addstr(9, 24, "YOUR SCORE: %s" % score, curses.color_pair(0))

    def draw_game_over(self, score):
        for row in range(20):
            for col in range(21):
                self.window.addstr(row + 3 , col + 1, ".", curses.color_pair(7))
        self.window.addstr(12, 4, "GAME OVER :(", curses.color_pair(9))
        self.window.addstr(14, 4, "YOUR SCORE: %s" % score, curses.color_pair(9))
        self.window.getch()
        time.sleep(5)


class Game:

    def __init__(self, render, window):
        self._window = window
        self._render = render
        self._board = Board()
        self.start_y = 0
        self.start_x = 4
        self._figure = GameElement.generate_figure(self.start_y, self.start_x)
        self._next_figure = GameElement.generate_figure(self.start_y, self.start_x)
        self._game_end = False
        self._game_running = True
        self._round = 0
        self._score = 0
        self._iterations = 0

    def increment_score(self, value=1):
        self._score += value

    def check_if_intersect(self, board_line, element):
        if board_line != "x":
            if element == 0:
                return False
            if element == 1:
                return True
        return False

    def move_down(self):
        contact_detected = self.check_intersection(self._board, self._figure)
        if not contact_detected:
            self._figure.move_down(self._board.height)

    def check_intersection(self, board, element):
        element_complete_path = element.pos_y + len(element.silhouette)
        if element_complete_path == board.height:
            return True
        elif board._field and element_complete_path <= board.height - 1:
            reverse_silhouette = element.silhouette[::-1]
            results = []
            for number, row in enumerate(reverse_silhouette):
                field_row = element_complete_path - number
                element_width = element.pos_x + element.width()
                row_slice = board._field[field_row][element.pos_x:element_width]
                check_tuples = list(zip(row_slice, row))
                r = [self.check_if_intersect(*i) for i in check_tuples]
                results.extend(r)
            return any(results)
        return False

    def _get_keyboard_input(self, event):
            if event == KEY_UP:
                if self._figure.pos_y + self._figure.height() <= self._board.height - 1:
                    self._figure.rotate(self._board.width, self._board.height)
                    if self.check_intersection(self._board, self._figure) and self._figure.pos_y + self._figure.height() <= self._board.height - 1:
                        self._figure.rotate(self._board.width, self._board.height)
            elif event == KEY_LEFT:
                self._figure.move_left()
                if self.check_intersection(self._board, self._figure):
                    self._figure.reset_position()
            elif event == KEY_RIGHT:
                self._figure.move_right(self._board.width)
                if self.check_intersection(self._board, self._figure):
                    self._figure.reset_position()
            elif event == KEY_DOWN:
                self.move_down()
            elif event == ord("r"):
                self.restart_round()
            elif event == ord("q"):
                self.quit()

    def quit(self):
        self._game_end = True
        self._game_running = False

    def restart_round(self):
        self._game_running = False
        self._round = 0
        self._score = 0
        self._iterations = 0
        self._figure = GameElement.generate_figure(self.start_y, self.start_x)
        self._next_figure = GameElement.generate_figure(self.start_y, self.start_x)


    def game_over(self):
        self._game_running = False
        self._game_end = True
        self._render.draw_game_over(self._score)

    def next_round(self, board):
        self._figure = self._next_figure
        self._next_figure = GameElement.generate_figure(self.start_y, self.start_x)
        self._board.update_board(board)
        lines_removed = self._board.check_matches()
        self.increment_score(lines_removed * self._board.width)
        self._round += 1

    def next_iteration(self):
        self._figure.set_down()

    def start_game(self):
        board = self._board.generate_board()
        auto_drop = 0
        prev_board = board
        auto_drop_threshold = 12
        while self._game_running:
            event = self._window.getch()
            auto_drop += 1
            self._get_keyboard_input(event)
            contact_detected = self.check_intersection(self._board, self._figure)
            board = self._board.merge_map(self._figure)
            if board != prev_board:
                self._render.draw_board(board)
                self._render.draw_next_element(self._next_figure)
                self._render.draw_score(self._score, self._round)
            if auto_drop == auto_drop_threshold:
                auto_drop = 0
                self._iterations += 1
                if not contact_detected and self._figure.pos_y + self._figure.height() <= self._board.height - 1:
                    self.next_iteration()
                elif contact_detected and self._figure.pos_y in [0, 1, 2]:
                    self.game_over()
                else:
                    self.next_round(board)
                    self.increment_score(1)
            if (self._round % 5 == 0) and auto_drop_threshold >= 5:
                auto_drop_threshold -= 1

    def run(self):
        while not self._game_end:
            self._game_running = True
            self._score = 0
            self._round = 1
            self._iterations = 0
            self.start_game()


def main(window):
    render = Render(window)
    game = Game(render, window)
    game.run()


if __name__ == "__main__":
    curses.initscr()
    curses.start_color()
    curses.beep()
    curses.beep()
    try:
        window = curses.newwin(HEIGHT, WIDTH, 0, 0)
        window.timeout(TIMEOUT)
        window.keypad(1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        main(window)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        curses.endwin()

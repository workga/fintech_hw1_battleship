import curses
from random import randint, shuffle
from collections import deque
import os
import pickle

from config import *
from field import Field


class Battleship:
    def __init__(self, height, width, load=False):
        self.height = height
        self.width = width

        self.cursor_y = 0
        self.cursor_x = 0

        if os.path.isfile(f"./.battleship.{self.height}x{self.width}.saved"):
            self.load()
        else:
            self.left_field = Field(self.height, self.width)
            self.right_field = Field(self.height, self.width)
            self.init_AI()

    def save(self):
        data = {
            "left_field": self.left_field,
            "right_field": self.right_field,
            "ai_queue": self.ai_queue,
        }

        with open(f"./.battleship.{self.height}x{self.width}.saved", "wb") as f_data:
            pickle.dump(data, f_data)

    def load(self):
        data = None

        with open(f"./.battleship.{self.height}x{self.width}.saved", "rb") as f_data:
            data = pickle.load(f_data)

        self.left_field = data["left_field"]
        self.right_field = data["right_field"]
        self.ai_queue = data["ai_queue"]

    def delete(self):
        if os.path.isfile(f"./.battleship.{self.height}x{self.width}.saved"):
            os.remove(f"./.battleship.{self.height}x{self.width}.saved")

    def get_fields_size(self):
        return self.height, self.width

    def get_cursor_pos(self):
        return self.cursor_y, self.cursor_x

    def get_statuses_as_str(self):
        left_area = self.left_field.get_ships_area()
        right_area = self.right_field.get_ships_area()

        if right_area == 0:
            return ("Game over! You won! (press any key)", "")
        elif left_area == 0:
            return ("Game over! Computer won! (press any key)", "")
        else:
            return (f"""{left_area} remains""", f"""{right_area} remains""")

    def get_fields_as_str(self):
        return self.left_field.as_str(), self.right_field.as_str(hidden=(not DEBUG))

    def handle_input(self, ch):
        if ch in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
            self.move_cursor(ch)
        elif ch == CONTROL_BOMB:
            self.make_move()

    def move_cursor(self, char):
        match char:
            case curses.KEY_LEFT:
                self.cursor_x = max(0, self.cursor_x - 1)
            case curses.KEY_RIGHT:
                self.cursor_x = min(self.width - 1, self.cursor_x + 1)
            case curses.KEY_UP:
                self.cursor_y = max(0, self.cursor_y - 1)
            case curses.KEY_DOWN:
                self.cursor_y = min(self.height - 1, self.cursor_y + 1)

    def init_AI(self):
        targets = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                targets.append((y, x))
        shuffle(targets)

        self.ai_queue = deque(targets)

    def AI_make_decision(self):
        y, x = self.ai_queue.pop()
        return y, x

    def make_move(self):
        ai_cursor_y, ai_cursor_x = self.AI_make_decision()

        self.right_field.bomb(self.cursor_y, self.cursor_x)
        self.left_field.bomb(ai_cursor_y, ai_cursor_x)

    def is_over(self):
        return self.left_field.is_defeated() or self.right_field.is_defeated()

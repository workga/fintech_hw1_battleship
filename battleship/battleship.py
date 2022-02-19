import curses
from random import randint

import config
from field import Field


class Battleship():
    """
    This class implements game logic.
    """
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.fields = [Field(self.height, self.width) for i in range(2)]

        self.cursor_y = 0
        self.cursor_x = 0

    def as_str(self):
        return "\n\n".join([self.fields[0].as_str(), \
                            self.fields[1].as_str(hidden=(not config.DEBUG))])
    
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

    def AI_make_decision(self):
        # use some algorithm
        y, x = randint(0, self.height - 1), randint(0, self.width - 1)
        return y, x

    def make_move(self):
        self.fields[1].bomb(self.cursor_y, self.cursor_x)
        ai_y, ai_x = self.AI_make_decision()
        self.fields[0].bomb(ai_y, ai_x)


    def is_over(self):
        return self.fields[0].defeated or self.fields[1].defeated
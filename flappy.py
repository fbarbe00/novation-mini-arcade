import random
from launchgame import LaunchGame
import logging


class FlappyBird(LaunchGame):
    """Basic implementation of Flappy Bird."""

    def __init__(self):
        super().__init__("Flappy Bird", 1)
        self.reset()

    def reset(self):
        super().reset()
        self.y = 3
        self.tubes = [[8, 3], [11, 3], [14, 3]]
        self.timer1 = 0
        self.timer2 = 0

    def step(self, evt, delta):
        if evt != [] and evt[0][2] > 0 and self.y > 0:
            self.y -= 1

        if self.y > 7:
            logging.info("Game over, you smashed into the ground!")
            self.game_over = True
            return

        for t in self.tubes:
            if t[0] == 1 and abs(self.y - t[1]) > 1:
                logging.info("Game over, you hit a tube!")
                self.game_over = True
                return

        self.timer1 += delta
        self.timer2 += delta
        if self.timer1 / 30000000 > 0.7 * (1 - self.scores[0] / 100):
            for t in self.tubes:
                if t[0] == 0:
                    t[0] = 8
                    t[1] = random.randint(1, 5)
                elif t[0] == 1:
                    self.increase_score(1)
                    t[0] -= 1
                else:
                    t[0] -= 1
            self.timer1 = 0
        if self.timer2 / 30000000 > 0.5:
            self.y += 1
            self.timer2 = 0

        self.paint_next(1, self.y, 0, 3)
        for t in self.tubes:
            for i in range(0, 8):
                if not abs(i - t[1]) <= 1:
                    self.paint_next(t[0], i, 3, 0)


game = FlappyBird()
game.run()

import time
import random
import logging
from launchgame import LaunchGame


class Pong(LaunchGame):
    """Basic implementation of Pong."""

    def __init__(self):
        super().__init__("Pong", 2, has_high_score=False, cumulative_score=True)
        self.reset()

    def new_ball(self):
        """Resets the ball to the center of the board and gives it a random direction."""
        self.ball = [random.randint(3, 4), random.randint(3, 4)]
        self.ball_dir = [random.choice([-1, 1]), random.choice([-1, 1])]

    def reset(self):
        super().reset()
        self.timer = 0
        self.elapsed_time = 0
        self.x1 = 4
        self.x2 = 4
        self.new_ball()

    def paint_win_point(self, ball_x, ball_y):
        """Custom animation for when a player scores a point."""
        direction = -1 if ball_y > 4 else 1
        for i in range(0, 14):
            for j in range(0, 2):
                self.lp.LedCtrlXY(ball_x + j, (ball_y + i * direction), 0, 0)
                self.lp.LedCtrlXY(
                    ball_x + j,
                    (ball_y + i * direction) - direction,
                    (i % 4),
                    ((i + 1) % 4),
                )
                self.lp.LedCtrlXY(
                    ball_x + j,
                    (ball_y + i * direction) - 2 * direction,
                    (i % 4),
                    ((i + 1) % 4),
                )
                self.lp.LedCtrlXY(
                    ball_x + j,
                    (ball_y + i * direction) - 3 * direction,
                    (i % 4),
                    ((i + 1) % 4),
                )
            time.sleep(0.08)

        self.lp.LedAllOn(0)
        self.prev_state = set()
        self.next_state = set()

    def step(self, evt, delta):
        # CONTROLS
        if evt != [] and evt[0][2] > 0:
            if (evt[0][1] <= 115 and evt[0][1] >= 112) and self.x1 > 1:
                self.x1 -= 1
            elif evt[0][1] > 115 and self.x1 < 6:
                self.x1 += 1
            elif evt[0][1] < 4 and self.x2 > 1:
                self.x2 -= 1
            elif evt[0][1] >= 4 and evt[0][1] < 8 and self.x2 < 6:
                self.x2 += 1
        if self.scores[0] >= 8 or self.scores[1] >= 8:
            self.game_over = True
            logging.info(
                "Game over! Player 1: "
                + str(self.scores[0])
                + " Player 2: "
                + str(self.scores[1])
            )
            return
        # make it proportional to elapsed time
        self.timer += delta
        if self.timer > 50000000 / (self.elapsed_time / 10 + 1):
            self.timer = 0
            if self.elapsed_time > 4:
                self.ball[0] += self.ball_dir[0]
                self.ball[1] += self.ball_dir[1]
                if self.ball[1] == 0 and abs(self.ball[0] - self.x2) <= 1:
                    new_pos = [
                        self.ball[0] - self.ball_dir[0],
                        self.ball[1] - self.ball_dir[1],
                    ]
                    self.ball_dir[1] *= -1
                    self.ball_dir[0] *= (
                        self.ball[0] - self.x2 if self.x2 - self.ball[0] != 0 else 1
                    )
                    self.ball = new_pos
                    self.ball[0] += self.ball_dir[0]
                    self.ball[1] += self.ball_dir[1]
                elif self.ball[1] == 7 and abs(self.ball[0] - self.x1) <= 1:
                    new_pos = [
                        self.ball[0] - self.ball_dir[0],
                        self.ball[1] - self.ball_dir[1],
                    ]
                    self.ball_dir[1] *= -1
                    self.ball_dir[0] *= (
                        self.ball[0] - self.x1 if self.x1 - self.ball[0] != 0 else 1
                    )
                    self.ball = new_pos
                    self.ball[0] += self.ball_dir[0]
                    self.ball[1] += self.ball_dir[1]
                elif self.ball[0] <= 0:
                    self.ball[0] = 0
                    self.ball_dir[0] *= -1
                elif self.ball[0] >= 7:
                    self.ball[0] = 7
                    self.ball_dir[0] *= -1
                elif self.ball[1] <= -1:
                    logging.info("Player 2 scored!")
                    self.paint_win_point(self.ball[0], self.ball[1])
                    self.increase_score(1, 1)
                    self.new_ball()
                    self.ball_dir = [random.choice([-1, 1]), random.choice([-1, 1])]
                    self.elapsed_time = 0
                elif self.ball[1] >= 8:
                    logging.info("Player 1 scored!")
                    self.paint_win_point(self.ball[0], self.ball[1])
                    self.increase_score(1, 0)
                    self.ball = [random.randint(3, 4), random.randint(4, 5)]
                    self.ball_dir = [random.choice([-1, 1]), random.choice([-1, 1])]
                    self.elapsed_time = 0
                elif random.randint(0, 1000) == 0:
                    self.ball_dir[0] += random.choice([-1, 1])
                    self.ball_dir[1] += random.choice([-1, 1])

            self.elapsed_time += 1

        if self.elapsed_time > 4 or (self.elapsed_time % 2 == 1):
            self.paint_next(self.ball[0], self.ball[1], 3, 3)
        self.paint_next(self.x1, 7, 0, 3)
        self.paint_next(self.x1 - 1, 7, 0, 3)
        self.paint_next(self.x1 + 1, 7, 0, 3)
        self.paint_next(self.x2, 0, 3, 0)
        self.paint_next(self.x2 - 1, 0, 3, 0)
        self.paint_next(self.x2 + 1, 0, 3, 0)


game = Pong()
game.run()

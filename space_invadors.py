import random
from launchgame import LaunchGame
import logging


class SpaceInvaders(LaunchGame):
    def __init__(self):
        LaunchGame.__init__(
            self,
            game_name="Space Invaders",
            num_players=1,
            has_high_score=True,
            cumulative_score=False,
        )
        self.reset()

    def reset(self):
        super().reset()
        self.x = 4
        self.timer1 = 0
        self.timer2 = 0
        self.aliens = [[0, 0], [2, 0], [4, 0], [6, 0]]
        self.alien_colors = [[1, 1], [1, 3], [2, 2], [3, 1]]
        self.shoot = [-1, 8]

    def step(self, evt, delta):
        # CONTROLS
        if evt != [] and evt[0][2] > 0:
            if (evt[0][1] <= 115 and evt[0][1] >= 112) and self.x > 0:
                self.x -= 1
            elif evt[0][1] > 115 and self.x < 7:
                self.x += 1
            elif self.shoot[1] == 8:
                self.shoot = [self.x, 5]
        for a in self.aliens:
            if a[1] == 7:
                self.game_over = True
                return

        # check with clock
        if self.shoot in self.aliens:
            self.alien_colors.remove(self.alien_colors[self.aliens.index(self.shoot)])
            self.aliens.remove(self.shoot)
            self.shoot = [-1, 8]
            self.increase_score(1)
        self.timer1 += delta
        if self.timer1 / 31000000 > 0.9 * (1 - self.scores[0] / 100):
            self.timer1 = 0
            for a in self.aliens:
                if random.randint(0, 5) == 0:
                    a[1] += 1
                if random.randint(0, 8) == 0:
                    new_x = a[0] + random.randint(-1, 1)
                    while (
                        ([new_x, a[1]] in self.aliens and new_x != a[0])
                        or new_x < 0
                        or new_x > 7
                    ):
                        new_x = a[0] + random.randint(-1, 1)
                    a[0] = new_x
            # randomly add a new alien
            if random.randint(0, len(self.aliens)) == 0:
                new_x = random.randint(0, 7)
                while [new_x, 0] in self.aliens:
                    new_x = random.randint(0, 7)
                self.aliens.append([new_x, 0])
                self.alien_colors.append([random.randint(1, 3), random.randint(1, 3)])
        self.timer2 += delta
        if self.timer2 / 50000000 > 0.1:
            self.timer2 = 0
            if self.shoot[1] < 8:
                self.shoot[1] -= 1
            if self.shoot[1] < 0:
                self.shoot = [-1, 8]

        self.paint_next(self.x, 6, 0, 3)
        for a in self.aliens:
            self.paint_next(
                a[0],
                a[1],
                self.alien_colors[self.aliens.index(a)][0],
                self.alien_colors[self.aliens.index(a)][1],
            )
        if self.shoot[1] < 8:
            self.paint_next(self.shoot[0], self.shoot[1], 3, 3)


game = SpaceInvaders()
game.run()

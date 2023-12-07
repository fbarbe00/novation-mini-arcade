import random
import logging
import numpy as np
import time
from launchgame import LaunchGame


class Tetris(LaunchGame):
    def __init__(self):
        super().__init__("Tetris", 1)
        self.define_blocks()
        self.reset()

    def new_block(self):
        self.current_block = np.array(random.choice(self.blocks))
        self.current_block_color = [random.randint(1, 3), random.randint(0, 3)]
        # randomly move block to the right
        self.current_block[:, 0] += random.randint(
            0, 7 - np.max(self.current_block[:, 0])
        )
        # randomly rotate block
        for i in range(0, random.randint(0, 3)):
            self.rotate_block()

    def reset(self):
        super().reset()
        self.new_block()
        self.timer = 0
        self.fallen_blocks = np.zeros((8, 8), dtype=object)
        self.level = 1
        self.blocks_passed = 0

    def define_blocks(self):
        self.blocks = [
            [[0, 0], [1, 0], [2, 0], [3, 0]],
            [[0, -1], [0, 0], [1, -1], [1, 0]],
            [[0, -1], [1, -1], [2, -1], [1, 0]],
            [[0, -1], [1, -1], [2, -1], [2, 0]],
            [
                [
                    0,
                    -1,
                ],
                [1, -1],
                [2, -1],
                [0, 0],
            ],
            [[0, -1], [1, -1], [1, 0], [2, 0]],
            [[0, -1], [1, -1], [1, 0], [2, -1]],
        ]

    def rotate_block(self):
        translated_coords = self.current_block - np.mean(self.current_block, axis=0)
        rotation_matrix = np.array([[0, -1], [1, 0]])

        # Apply the rotation matrix to the translated coordinates
        rotated_coords = np.dot(translated_coords, rotation_matrix.T)

        # Translate the coordinates back to their original position
        rotated_coords += np.mean(self.current_block, axis=0)

        rotated_coords = np.round(rotated_coords, decimals=1)
        # convert to ints
        rotated_coords = rotated_coords.astype(int)
        if (
            np.any(rotated_coords[:, 0] < 0)
            or np.any(rotated_coords[:, 0] > 7)
            or np.any(rotated_coords[:, 1] > 7)
            or np.any(self.fallen_blocks[rotated_coords[:, 0], rotated_coords[:, 1]])
            or len(np.unique(rotated_coords, axis=0)) != len(rotated_coords)
        ):
            logging.debug("Can't rotate")
            return

        self.current_block = rotated_coords

    def blink_row(self, row):
        for j in range(2):
            for i in range(0, 8):
                self.lp.LedCtrlXY(i, row + 1, 3, 3)
            time.sleep(0.2)
            for i in range(0, 8):
                self.lp.LedCtrlXY(i, row + 1, 0, 0)
                self.prev_state.add((i, row + 1, 0, 0))
            time.sleep(0.2)

    def check_for_full_rows(self):
        for b in self.current_block:
            # check if all values are nonzero
            if np.all(self.fallen_blocks[:, b[1]]):
                logging.debug("Full row (" + str(b[1]) + ")")
                # full row
                # self.blink_row(b[1])
                # move everything above one down
                self.fallen_blocks[:, 1 : (b[1] + 1)] = self.fallen_blocks[:, 0 : b[1]]
                self.fallen_blocks[:, 0] = 0
                # increase score
                self.increase_score(1)
                self.blocks_passed += 2
                time.sleep(0.5)
                return True
        return False

    def step(self, evt, delta):
        super().step(evt, delta)

        can_move_left = min(self.current_block[:, 0]) > 0 and not np.any(
            self.fallen_blocks[self.current_block[:, 0] - 1, self.current_block[:, 1]]
        )
        can_move_right = max(self.current_block[:, 0]) < 7 and not np.any(
            self.fallen_blocks[self.current_block[:, 0] + 1, self.current_block[:, 1]]
        )
        # CONTROLS
        x = 0
        y = 0
        if evt != [] and evt[0][2] > 0:
            if (evt[0][1] <= 115 and evt[0][1] >= 112) and can_move_left:
                x -= 1
            elif (evt[0][1] > 115 and evt[0][1] < 120) and can_move_right:
                x += 1
            elif evt[0][1] == 120:
                y += 1
            elif evt[0][1] < 111:
                # rotate
                self.rotate_block()

        self.timer += delta
        if self.timer > 100000000 / (self.level * 5):
            self.timer = 0
            y += 1

        if y > 0:
            for b in self.current_block:
                b[0] = int(b[0] + x)
                if b[1] >= 7 or self.fallen_blocks[b[0], b[1] + 1]:
                    logging.debug("Block hit something")
                    self.blocks_passed += 1
                    for b in self.current_block:
                        if b[1] <= 0:
                            self.game_over = True
                            break
                        self.fallen_blocks[b[0], b[1]] = self.current_block_color

                    multiple_rows = self.check_for_full_rows()
                    while multiple_rows:
                        multiple_rows = self.check_for_full_rows()
                        self.increase_score(1)
                    self.new_block()
                    break
            x = 0

        if self.blocks_passed >= 15:
            self.blocks_passed = 0
            self.level += 1
            self.lp.LedCtrlXY(8, 9 - self.level, self.level, self.level)

        # add everything that needs to be seen:
        for b in self.current_block:
            b[1] = int(b[1] + y)
            b[0] = int(b[0] + x)
            self.paint_next(
                b[0], b[1], self.current_block_color[0], self.current_block_color[1]
            )
        for i in range(0, 8):
            for j in range(0, 8):
                if self.fallen_blocks[i, j]:
                    self.paint_next(
                        i, j, self.fallen_blocks[i, j][0], self.fallen_blocks[i, j][1]
                    )


game = Tetris()
game.run()

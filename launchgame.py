import novation_launchpad
import time
import logging


class LaunchGame:
    """Base class for all games.
    This class provides a framework for creating games for the Novation Launchpad MINI.
    It provides a number of useful methods for painting the board, handling button presses,
    and running the game loop.
    """

    def __init__(
        self,
        game_name: str = "Launchpad Game",
        num_players: int = 1,
        lp: novation_launchpad.Launchpad = None,
        has_high_score: bool = True,
        cumulative_score: bool = False,
    ):
        """Initializes a LaunchGame object.
        Args:
            game_name (str): The name of the game.
            num_players (int): The number of players.
            lp (Launchpad): The Launchpad object to use. If None, a new one will be created.
            has_high_score (bool): Whether or not the game should be displayed.
            cumulative_score (bool): Whether or not the score should be shown as a cumulative.
        """
        if lp is None:
            self.lp = novation_launchpad.Launchpad()
            self.lp.Open()
        self.lp.ButtonFlush()
        self.name = game_name
        self.num_players = num_players
        self.scores = [0] * num_players
        self.has_high_score = has_high_score
        self.cumulative_score = cumulative_score
        self.high_scores = [0] * num_players
        self.game_over = False

        self.prev_state = set()
        self.next_state = set()

    def reset(self):
        """Resets the game.
        This method resets all the game variables and clears the board.
        """
        self.scores = [0] * self.num_players
        self.game_over = False
        self.lp.LedAllOn(0)
        self.lp.ButtonFlush()
        self.prev_state = set()
        self.next_state = set()

    def paint_next(self, x, y, r, g):
        """Paints the given LED on the next frame.
        This method adds the given LED to the next frame to be painted.
        All other LEDs will be cleared.
        Args:
            x (int): The x coordinate of the LED.
            y (int): The y coordinate of the LED.
            r (int): The red value of the LED.
            g (int): The green value of the LED.
        """
        if y >= 0 and y < 8 and x >= 0 and x < 8:
            self.next_state.add(
                (x, y + 1, r, g)  # +1 because the first row is the score
            )

    def paint(self):
        """Paints the next frame."""
        to_unpaint = self.prev_state.difference(self.next_state)
        for led in to_unpaint:
            self.lp.LedCtrlXY(led[0], led[1], 0, 0)
        to_paint = self.next_state.difference(self.prev_state)
        for led in to_paint:
            self.lp.LedCtrlXY(led[0], led[1], led[2], led[3])
        self.prev_state = self.next_state.copy()
        self.next_state.clear()

    def paint_score(self):
        """Paints the score on the board."""
        score_1 = self.scores[0]
        for i in range(0, 8):
            if (score_1 % 9) - 1 == i or (score_1 // 9) - 1 == i:
                self.lp.LedCtrlXY(i, 0, 3, 3)
            elif not self.cumulative_score:
                self.lp.LedCtrlXY(i, 0, 0, 0)
        if self.num_players == 2:
            score_2 = self.scores[1]
            for i in range(1, 9):
                if (score_2 % 9) - 1 >= (8 - i) or (score_2 // 9) - 1 >= (8 - i):
                    self.lp.LedCtrlXY(8, i, 3, 3)
                elif not self.cumulative_score:
                    self.lp.LedCtrlXY(8, i, 0, 0)

        if self.num_players > 2:
            raise ValueError("Can only paint scores for 1 or 2 players")

    def paint_high_score(self):
        """Paints the high score on the board."""
        for i in range(0, 8):
            if (self.high_scores[0] % 9) - 1 == i or (
                self.high_scores[0] // 9
            ) - 1 == i:
                self.lp.LedCtrlXY(i, 0, 0, 3)
            else:
                self.lp.LedCtrlXY(i, 0, 0, 0)
        if self.num_players == 2:
            for i in range(1, 9):
                if (self.high_scores[1] % 9) - 1 >= (8 - i) or (
                    self.high_scores[1] // 9
                ) - 1 >= (8 - i):
                    self.lp.LedCtrlXY(8, i, 0, 3)
                else:
                    self.lp.LedCtrlXY(8, i, 0, 0)

    def update_score(self, score, player=0):
        """Updates the score for the given player.
        This method updates the score for the given player.
        If the score is higher than the current high score, the high score is updated.
        Args:
            score (int): The new score.
            player (int): The player whose score should be updated.
        """
        self.scores[player] = score
        if self.has_high_score:
            if score > self.high_scores[player]:
                self.high_scores[player] = score
        self.paint_score()

    def increase_score(self, amount, player=0):
        """Increases the score for the given player.
        This method increases the score for the given player by the given amount.
        If the score is higher than the current high score, the high score is updated.
        Args:
            amount (int): The amount to increase the score by.
            player (int): The player whose score should be updated.
        """
        self.scores[player] += amount
        if self.has_high_score:
            if self.scores[player] > self.high_scores[player]:
                self.high_scores[player] = self.scores[player]
        self.paint_score()

    def step(self, evt, delta):
        """Steps the game forward.
        This method should be overridden by subclasses to implement the game logic.
        Args:
            evt (list): The list of events from the Launchpad.
            delta (int): The time since the last step, in nanoseconds.
        """
        pass

    def animation_start_game(self):
        """Animates the start of the game."""
        if logging.getLogger().getEffectiveLevel() != logging.DEBUG:
            for i in range(3):
                logging.info("Game starting in " + str(3 - i))
                self.lp.LedCtrlChar(str(3 - i), 3 - 1, i, 1)
                time.sleep(1)

        self.lp.LedAllOn(0)

    def process_game_over(self):
        """Is called when the game is over."""
        logging.info("Game over!")
        self.lp.LedAllOn()

    def run_game(self):
        """Runs the game."""
        self.reset()
        self.animation_start_game()
        prev_time = time.time_ns()
        self.paint_score()
        if self.has_high_score:
            self.paint_high_score()
        while not self.game_over:
            evt = self.lp.EventRaw()
            delta = (time.time_ns() - prev_time) >> 2
            self.step(evt, delta)
            self.paint()

            prev_time = time.time_ns()

        self.process_game_over()

    def run(self):
        self.lp.ButtonFlush()
        logging.info("Press any button to start")
        while True:
            evt = self.lp.EventRaw()
            if evt != [] and evt[0][2] > 0:
                self.run_game()

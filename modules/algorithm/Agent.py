"""
This AI agent is based on Alpha-Beta minimax algorithm
"""
import random
from itertools import product


# check any five chessman (in a row/column/diagonal) from the selected chessman
# if 5 in 1 row/column/diagonal, then the game is over
# static method
def over(selected):
    for i, j in product(range(19), range(19)):
        if (
            i < 15
            and (i, j) in selected
            and (i + 1, j) in selected
            and (i + 2, j) in selected
            and (i + 3, j) in selected
            and (i + 4, j) in selected
        ):
            return True
        elif (
            j < 15
            and (i, j) in selected
            and (i, j + 1) in selected
            and (i, j + 2) in selected
            and (i, j + 3) in selected
            and (i, j + 4) in selected
        ):
            return True
        elif (
            i < 15
            and j < 15
            and (i, j) in selected
            and (i + 1, j + 1) in selected
            and (i + 2, j + 2) in selected
            and (i + 3, j + 3) in selected
            and (i + 4, j + 4) in selected
        ):
            return True
        elif (
            i > 3
            and j < 15
            and (i, j) in selected
            and (i - 1, j + 1) in selected
            and (i - 2, j + 2) in selected
            and (i - 3, j + 3) in selected
            and (i - 4, j + 4) in selected
        ):
            return True
    return False


class Agent:

    # constructor
    def __init__(self, ai_color, human_color, depth=1):
        assert depth % 2, "depth must be odd number"
        self.ai_color = ai_color
        self.human_color = human_color
        self.search_depth = depth
        self.ai = None
        self.human_selected = None
        self.ai_selected = None
        self.next_step = None

        # [score (arrangement of chessman)]
        # give a score to each kind of arrangement of chessman, the arrangement with the larger score
        # will be selected first (has the largest chance to result)
        self.score = [
            (10, (0, 1, 1, 0, 0)),
            (10, (0, 0, 1, 1, 0)),
            (50, (1, 1, 0, 1, 0)),
            (100, (0, 0, 1, 1, 1)),
            (100, (1, 1, 1, 0, 0)),
            (1000, (0, 1, 1, 1, 0)),
            (1000, (0, 1, 0, 1, 1, 0)),
            (1000, (0, 1, 1, 0, 1, 0)),
            (1000, (1, 1, 1, 0, 1)),
            (1000, (1, 1, 0, 1, 1)),
            (1000, (1, 0, 1, 1, 1)),
            (1000, (1, 1, 1, 1, 0)),
            (1000, (0, 1, 1, 1, 1)),
            (10000, (0, 1, 1, 1, 1, 0)),
            (10000000, (1, 1, 1, 1, 1)),
        ]

        self.alpha = -10000000  # means negative infinity
        self.beta = 10000000  # means positive infinity
        self.chess_board = [(i, j) for i, j in product(range(19), range(19))]

    # invoke agent
    def action(self, history_record):
        self.ai = []
        self.human_selected = []
        self.ai_selected = []
        for item in history_record:
            self.ai_selected.append((item[0], item[1]))
            if item[-1] == self.ai_color:
                self.ai.append((item[0], item[1]))
            elif item[-1] == self.human_color:
                self.human_selected.append((item[0], item[1]))
        while True:
            self.next_step = random.choice(range(19)), random.choice(range(19))
            if self.next_step not in self.ai_selected:
                break
        self.minimax_prune(True, self.search_depth, self.alpha, self.beta)
        return self.next_step

    # search the minimum negative value, perform alpha-beta pruning
    def minimax_prune(self, agent_round, depth, alpha, beta):
        if over(self.ai) or over(self.human_selected) or depth == 0:
            return self.decision(agent_round)
        temp = list(set(self.chess_board).difference(set(self.ai_selected)))
        temp = self.rearrange(temp)
        for next_step in temp:
            if not self.neighbor(next_step):
                continue
            # if it's AI round
            if agent_round:
                self.ai.append(next_step)
            else:
                self.human_selected.append(next_step)
            self.ai_selected.append(next_step)
            value = -self.minimax_prune(not agent_round, depth - 1, -beta, -alpha)
            if agent_round:
                self.ai.remove(next_step)
            else:
                self.human_selected.remove(next_step)
            self.ai_selected.remove(next_step)
            if value > alpha:
                if depth == self.search_depth:
                    self.next_step = next_step
                if value >= beta:
                    return beta
                alpha = value
        return alpha

    # rearrange the positions that haven't been selected
    def rearrange(self, not_selected):
        last_step = self.ai_selected[-1]
        for _ in not_selected:
            for i, j in product(range(-1, 2), range(-1, 2)):
                if i == 0 and j == 0:
                    continue
                next_step = (last_step[0] + i, last_step[1] + j)
                if next_step in not_selected:
                    not_selected.remove(next_step)
                    not_selected.insert(0, next_step)
        return not_selected

    # determine if the neighbor chessman has the same color as the current one
    def neighbor(self, next_step):
        for i, j in product(range(-1, 2), range(-1, 2)):
            if i == 0 and j == 0:
                continue
            if (next_step[0] + i, next_step[1] + j) in self.ai_selected:
                return True
        return False

    # calculate the score
    def score_cal(self, i, j, x_direction, y_direction, l1, l2, all_score_sum):
        score_sum = 0
        max_score = (0, None)
        for each in all_score_sum:
            for item in each[1]:
                if (
                    i == item[0]
                    and j == item[1]
                    and x_direction == each[2][0]
                    and y_direction == each[2][1]
                ):
                    return 0, all_score_sum
        for number_offset in range(-5, 1):
            position = []
            for position_offset in range(6):
                x, y = (
                    i + (position_offset + number_offset) * x_direction,
                    j + (position_offset + number_offset) * y_direction,
                )
                if (x, y) in l2:
                    position.append(2)
                elif (x, y) in l1:
                    position.append(1)
                else:
                    position.append(0)
            shape_len5 = tuple(position[0:-1])
            shape_len6 = tuple(position)
            for score, shape in self.score:
                if shape_len5 == shape or shape_len6 == shape:
                    if score > max_score[0]:
                        max_score = (
                            score,
                            (
                                (
                                    i + (0 + number_offset) * x_direction,
                                    j + (0 + number_offset) * y_direction,
                                ),
                                (
                                    i + (1 + number_offset) * x_direction,
                                    j + (1 + number_offset) * y_direction,
                                ),
                                (
                                    i + (2 + number_offset) * x_direction,
                                    j + (2 + number_offset) * y_direction,
                                ),
                                (
                                    i + (3 + number_offset) * x_direction,
                                    j + (3 + number_offset) * y_direction,
                                ),
                                (
                                    i + (4 + number_offset) * x_direction,
                                    j + (4 + number_offset) * y_direction,
                                ),
                            ),
                            (x_direction, y_direction),
                        )
        if max_score[1] is not None:
            for each in all_score_sum:
                for p1 in each[1]:
                    for p2 in max_score[1]:
                        if p1 == p2 and max_score[0] > 10 and each[0] > 10:
                            score_sum += max_score[0] + each[0]
            all_score_sum.append(max_score)
        return score_sum + max_score[0], all_score_sum

    # the agent should make decision base on its total score when it's AI's round
    def decision(self, ai_round):
        if ai_round:
            l1 = self.ai
            l2 = self.human_selected
        else:
            l1 = self.human_selected
            l2 = self.ai
        add_scores = []
        add = 0
        for item in l1:
            score, add_scores = self.score_cal(
                item[0], item[1], 0, 1, l1, l2, add_scores
            )
            add += score
            score, add_scores = self.score_cal(
                item[0], item[1], 1, 0, l1, l2, add_scores
            )
            add += score
            score, add_scores = self.score_cal(
                item[0], item[1], 1, 1, l1, l2, add_scores
            )
            add += score
            score, add_scores = self.score_cal(
                item[0], item[1], -1, 1, l1, l2, add_scores
            )
            add += score
        reduce_scores = []
        reduce = 0
        for item in l2:
            score, reduce_scores = self.score_cal(
                item[0], item[1], 0, 1, l2, l1, reduce_scores
            )
            reduce += score
            score, reduce_scores = self.score_cal(
                item[0], item[1], 1, 0, l2, l1, reduce_scores
            )
            reduce += score
            score, reduce_scores = self.score_cal(
                item[0], item[1], 1, 1, l2, l1, reduce_scores
            )
            reduce += score
            score, reduce_scores = self.score_cal(
                item[0], item[1], -1, 1, l2, l1, reduce_scores
            )
            reduce += score
        total_score = add - reduce * 0.1
        return total_score

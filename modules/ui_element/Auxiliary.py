"""
Some auxiliary functions
"""
import os
from itertools import product


# check if directory exists
def check_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return False
    return True


# check if the agent or human wins
def check_result(chessboard):
    # no one wins if the entire chessboard is full
    full = True
    for i, j in product(range(19), range(19)):
        if chessboard[i][j] is None:
            full = False
    if full:
        return "draw"
    # check if someone wins (5 chessman in a row shows) after adding this chessman
    for i, j in product(range(19), range(19)):
        # result with the right 4 chessmen
        if i < 15:
            chessmen = [
                chessboard[i][j],
                chessboard[i + 1][j],
                chessboard[i + 2][j],
                chessboard[i + 3][j],
                chessboard[i + 4][j],
            ]
            if None not in chessmen:
                colors = [c.color for c in chessmen]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # result with the below 4 chessmen
        if j < 15:
            chessmen = [
                chessboard[i][j],
                chessboard[i][j + 1],
                chessboard[i][j + 2],
                chessboard[i][j + 3],
                chessboard[i][j + 4],
            ]
            if None not in chessmen:
                colors = [c.color for c in chessmen]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # result with the lower right 4
        if i < 15 and j < 15:
            chessmen = [
                chessboard[i][j],
                chessboard[i + 1][j + 1],
                chessboard[i + 2][j + 2],
                chessboard[i + 3][j + 3],
                chessboard[i + 4][j + 4],
            ]
            if None not in chessmen:
                colors = [c.color for c in chessmen]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # result with the lower left 4
        if i > 3 and j < 15:
            chessmen = [
                chessboard[i][j],
                chessboard[i - 1][j + 1],
                chessboard[i - 2][j + 2],
                chessboard[i - 3][j + 3],
                chessboard[i - 4][j + 4],
            ]
            if None not in chessmen:
                colors = [c.color for c in chessmen]
                if len(list(set(colors))) == 1:
                    return colors[0]
    return None


# convert image pixel to chessman position
def pixel2chess(point):
    x, y = point.x(), point.y()
    x = round((x - 50.0) / 30.0)
    y = round((y - 50.0) / 30.0)
    return x, y


# convert chessman position to image pixel
def chess2pixel(position):
    x = position[0] * 30 + 50
    y = position[1] * 30 + 50
    return x, y

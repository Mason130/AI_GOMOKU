"""configure UI"""
import os

# background images
Background = {
    "bg_game": os.path.join(os.getcwd(), "images/background/game_UI.png"),
    "bg_start": os.path.join(os.getcwd(), "images/background/main_UI.png"),
}

# button images
# default button: image_0
# mouse release the button: image_1
# mouse press the button: image_2
Button = {
    "start": [
        os.path.join(os.getcwd(), "images/buttons/start_0.png"),
        os.path.join(os.getcwd(), "images/buttons/start_1.png"),
        os.path.join(os.getcwd(), "images/buttons/start_2.png"),
    ],
    "home": [
        os.path.join(os.getcwd(), "images/buttons/home_0.png"),
        os.path.join(os.getcwd(), "images/buttons/home_1.png"),
        os.path.join(os.getcwd(), "images/buttons/home_2.png"),
    ],
}

# winner images
# white (human) first, black (AI)
Result = {
    "black": os.path.join(os.getcwd(), "images/result/black_win.png"),
    "white": os.path.join(os.getcwd(), "images/result/white_win.png"),
    "draw": os.path.join(os.getcwd(), "images/result/draw.png"),
}

# chessman images
Chessman = {
    "black": os.path.join(os.getcwd(), "images/chessman/black.png"),
    "white": os.path.join(os.getcwd(), "images/chessman/white.png"),
    "sign": os.path.join(os.getcwd(), "images/chessman/sign.png"),
}

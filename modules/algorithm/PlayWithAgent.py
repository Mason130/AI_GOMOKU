"""
Create the UI such that the human player could play with the AI agent
"""
from ..ui_element.Button import *
from ..ui_element.Chessman import *
from ..algorithm.Agent import Agent


class PlayWithAgent(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    send_back_signal = False

    # constructor
    def __init__(self, configure, parent=None):
        super(PlayWithAgent, self).__init__(parent)
        self.configure = configure
        self.setFixedSize(760, 650)
        self.setWindowTitle("COS470-GOMOKU")

        # background
        palette = QPalette()
        palette.setBrush(
            self.backgroundRole(), QBrush(QPixmap(configure.Background.get("bg_game")))
        )
        self.setPalette(palette)

        # buttons
        self.home = Button(configure.Button.get("home"), self)
        self.home.click_signal.connect(self.back_home)
        self.home.move(603, 250)

        # signal indicates the current chessman
        self.chessman_sign = QLabel(self)
        sign = QPixmap(configure.Chessman.get("sign"))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()

        # chessboard of the size of 19x19
        self.chessboard = [[None for _ in range(19)] for _ in range(19)]
        # record the history of used chessman
        self.history = []
        # if the game is running
        self.running = True
        # winner
        self.winner = None
        self.winner_name = None
        # human always play first (the one who plays first will definitely result in some case)
        self.human_color = "white"
        self.agent_color = "black"
        self.round = self.human_color
        # instantiate an AI agent
        self.agent_player = Agent(self.agent_color, self.human_color)

    # human plays after pressing the mouse
    def mousePressEvent(self, event):
        if (
            (event.buttons() != QtCore.Qt.LeftButton)
            or (self.winner is not None)
            or (self.round != self.human_color)
            or (not self.running)
        ):
            return
        # the range of chessboard
        if (
            50 <= event.x() <= 50 + 30 * 18 + 14
            and 50 <= event.y() <= 50 + 30 * 18 + 14
        ):
            pos = pixel2chess(event)
            # cannot reuse a chessboard position
            if self.chessboard[pos[0]][pos[1]]:
                return
            # instantiate a chessman
            c = Chessman(self.configure.Chessman.get(self.round), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # mark the chessman just be placed
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # record this chessman's position
            self.history.append([*pos, self.round])
            # check if agent or human wins
            self.winner = check_result(self.chessboard)
            if self.winner:
                self.game_over()
                return
            # human finishes playing, then AI's round
            self.next_step()

    # call agent to play after releasing the mouse
    def mouseReleaseEvent(self, event):
        if (
            (self.winner is not None)
            or (self.round != self.agent_color)
            or (not self.running)
        ):
            return
        self.agent_round()

    # close the window
    def closeEvent(self, event):
        if not self.send_back_signal:
            self.exit_signal.emit()

    # agent automatically plays after human
    def agent_round(self):
        if (
            (self.winner is not None)
            or (self.round == self.human_color)
            or (not self.running)
        ):
            return
        next_pos = self.agent_player.action(self.history)
        chessman = Chessman(self.configure.Chessman.get(self.round), self)
        chessman.move(QPoint(*chess2pixel(next_pos)))
        chessman.show()
        self.chessboard[next_pos[0]][next_pos[1]] = chessman
        # mark the chessman just be placed
        self.chessman_sign.show()
        self.chessman_sign.move(chessman.pos())
        self.chessman_sign.raise_()
        self.history.append([*next_pos, self.round])
        # check if agent or human wins
        self.winner = check_result(self.chessboard)
        if self.winner:
            self.game_over()
            return
        # AI plays after human, that is, change the chessman color
        self.next_step()

    def next_step(self):
        self.round = (
            self.human_color if self.round == self.agent_color else self.agent_color
        )

    # show the result when game is over
    # "human result" or "AI" result
    def game_over(self):
        self.running = False
        info_img = QPixmap(self.configure.Result.get(self.winner))
        self.winner_name = QLabel(self)
        self.winner_name.setPixmap(info_img)
        self.winner_name.resize(info_img.size())
        self.winner_name.move(50, 50)
        self.winner_name.show()

    # start the game
    def start_game(self):
        if self.running:
            return
        self.running = True
        self.round = self.human_color
        for i, j in product(range(19), range(19)):
            if self.chessboard[i][j]:
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None
        self.winner = None
        self.winner_name.close()
        self.winner_name = None
        self.history.clear()
        self.chessman_sign.hide()

    # go back to home UI
    def back_home(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()

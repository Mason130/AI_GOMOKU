"""
Main UI
"""
import sys
import configure
from modules.algorithm.PlayWithAgent import *


class MainUI(QWidget):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.gaming_ui = None
        self.setFixedSize(760, 650)
        self.setWindowTitle("COS470-GOMOKU")

        # background
        palette = QPalette()
        palette.setBrush(
            self.backgroundRole(), QBrush(QPixmap(configure.Background.get("bg_start")))
        )
        self.setPalette(palette)

        # buttons
        # start game
        self.ai_button = Button(configure.Button.get("start"), self)
        self.ai_button.move(260, 250)
        self.ai_button.show()
        self.ai_button.click_signal.connect(self.game_begin)

    def game_begin(self):
        self.close()
        self.gaming_ui = PlayWithAgent(configure)
        self.gaming_ui.exit_signal.connect(lambda: sys.exit())
        self.gaming_ui.back_signal.connect(self.show)
        self.gaming_ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    handle = MainUI()
    font = QFont()
    font.setPointSize(12)
    handle.setFont(font)
    handle.show()
    sys.exit(app.exec_())

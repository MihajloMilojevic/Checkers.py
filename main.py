from src.game import Checkers
from PyQt5.QtWidgets import QApplication, QPushButton, QFrame, QVBoxLayout

if __name__ == "__main__":
    app = QApplication([])
    frame = QFrame()
    frame.setGeometry(100, 100, 400, 400)
    button = QPushButton("Click me")
    button.setGeometry(100, 100, 200, 50)
    def onEnd(game):
        if game.state.winner is not None:
            button.setText(f"{game.state.winner} won")
            frame.setVisible(True)
    def run_game():
        frame.setVisible(False)
        game = Checkers(Checkers.TWO_PLAYERS)
        game.run(onEnd)
    button.clicked.connect(run_game)
    button.clicked.connect(lambda: print("Button clicked"))
    frame.setLayout(QVBoxLayout())
    frame.layout().addWidget(button)
    frame.show()
    quit(app.exec_())

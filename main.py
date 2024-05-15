from src.game import Checkers
from PyQt5.QtWidgets import QApplication, QPushButton, QFrame, QVBoxLayout

class State:
    game = None

if __name__ == "__main__":
    app = QApplication([])
    frame = QFrame()
    frame.setGeometry(100, 100, 400, 400)
    button = QPushButton("Click me")
    button.setGeometry(100, 100, 200, 50)
    def onEnd(game):
        if game.state.winner is not None:
            button.setText(f"{game.state.winner} won")
            #frame.setVisible(True)
    def run_game():
        #frame.setVisible(False)
        State.game = Checkers(Checkers.SINGLE_PLAYER)
        State.game.run(onEnd)
    button.clicked.connect(run_game)
    undo = QPushButton("Undo")
    def undo_move():
        if State.game is None:
            return
        State.game.undo()
    undo.clicked.connect(undo_move)
    frame.setLayout(QVBoxLayout())
    frame.layout().addWidget(button)
    frame.layout().addWidget(undo)
    frame.show()
    quit(app.exec_())

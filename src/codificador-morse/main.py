import sys
import threading
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from .encode.encoder import encode_message, play_encoded_message


class MorseCodeApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Codificador de Código Morse")
        self.resize(500, 350)
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Default ui setup.
        """
        layout = QVBoxLayout()

        # input
        self.input_label = QLabel("Digite o texto (Caracteres ASCII suportados):")
        layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ex: SOS")
        layout.addWidget(self.input_field)

        # encode button
        self.btn_encode = QPushButton("Codificar para Morse")
        self.btn_encode.clicked.connect(self.handle_encode)
        layout.addWidget(self.btn_encode)

        # output
        self.output_label = QLabel("Código Morse Gerado:")
        layout.addWidget(self.output_label)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setPlaceholderText("O resultado aparecerá aqui...")
        layout.addWidget(self.output_field)

        # audio button
        self.btn_play = QPushButton("Tocar Som")
        self.btn_play.clicked.connect(self.handle_play)
        self.btn_play.setEnabled(False)  # Disabled until has a valid code
        layout.addWidget(self.btn_play)

        self.setLayout(layout)

    def handle_encode(self) -> None:
        """
        Handle the text input to show the encoded message.
        """
        raw_msg = self.input_field.text()
        if not raw_msg:
            QMessageBox.warning(
                self, "Aviso", "Por favor, digite um texto para codificar."
            )
            return

        encoded_msg = encode_message(raw_msg)

        if encoded_msg:
            self.output_field.setPlainText(encoded_msg)
            self.btn_play.setEnabled(True)
        else:
            QMessageBox.critical(
                self,
                "Erro",
                "Texto contém caracteres não suportados pelo dicionário Morse.",
            )
            self.output_field.clear()
            self.btn_play.setEnabled(False)

    def handle_play(self) -> None:
        """
        Play the encoded message in audio interface with a new Thread.
        """
        msg = self.output_field.toPlainText()
        if msg:
            # deactive the button to avoid multiple executions
            self.btn_play.setEnabled(False)
            self.btn_play.setText("Tocando...")

            # use a thread to avoid ui blocking
            threading.Thread(
                target=self.play_audio_thread, args=(msg,), daemon=True
            ).start()

    def play_audio_thread(self, msg: str) -> None:
        """
        Play the message a enable the audio button.
        """
        try:
            play_encoded_message(msg)
        finally:
            self.btn_play.setEnabled(True)
            self.btn_play.setText("Tocar Som")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MorseCodeApp()
    window.show()
    sys.exit(app.exec())

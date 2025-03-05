from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt5 import uic
import sys
import asyncio
from googletrans import Translator, LANGUAGES

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("translate.ui", self)
        self.setWindowTitle("Translator App")

        # Define widgets
        self.trans_button = self.findChild(QPushButton, "pushButton")
        self.clear_button = self.findChild(QPushButton, "pushButton_2")

        self.combo_1 = self.findChild(QComboBox, "comboBox")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")

        self.text_1 = self.findChild(QTextEdit, "textEdit")
        self.text_2 = self.findChild(QTextEdit, "textEdit_2")

        # Click event for buttons
        self.trans_button.clicked.connect(self.translate)
        self.clear_button.clicked.connect(self.clear)

        # Add languages to combo boxes
        self.languages = LANGUAGES  # FIXED: Use module-level LANGUAGES
        self.language_list = list(self.languages.values())

        self.combo_1.addItems(self.language_list)
        self.combo_2.addItems(self.language_list)

        # Set default combo items
        self.combo_1.setCurrentText("turkish")
        self.combo_2.setCurrentText("english")

        # Show the app
        self.show()

    def clear(self):
        self.text_1.setText("")
        self.text_2.setText("")
        self.combo_1.setCurrentText("turkish")
        self.combo_2.setCurrentText("english")

    def translate(self):
        try:
            translator = Translator()

            # Get language keys
            from_lang = next(key for key, value in self.languages.items() if value == self.combo_1.currentText())
            to_lang = next(key for key, value in self.languages.items() if value == self.combo_2.currentText())

            text = self.text_1.toPlainText()

            if not text.strip():
                raise ValueError("Please enter text to translate!")

            # Run async translation
            translation = asyncio.run(translator.translate(text, src=from_lang, dest=to_lang))

            # Output to text box
            self.text_2.setText(translation.text)

        except Exception as e:
            QMessageBox.about(self, "Translator", f"Error: {str(e)}")

# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()




import sys
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QScrollArea, QMainWindow, QLabel, QFrame,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter
)
from PySide6.QtCore import Qt
import wikipedia
from year_finder import getWikiText, yearFinder


# from customwidgets import OnOffWidget


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.finalYaer = ""

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.

        # List of names, widgets are stored in a dictionary by these keys.
        widget_names = [
            "Heater", "Stove", "Living Room Light", "Balcony Light",
            "Fan", "Room Light", "Oven", "Desk Light",
            "Bedroom Heater", "Wall Switch"
        ]
        self.widgets = []

        self.text_widget = QLabel(self)
        self.text_widget.setWordWrap(True)
        self.text_widget.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.text_widget.setText("first line\nsecond line")
        self.text_widget.setAlignment(Qt.AlignLeft | Qt.AlignLeft)

        self.result_widget = QLabel(self)
        self.result_widget.setWordWrap(True)
        self.result_widget.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.result_widget.setText("")
        self.result_widget.setAlignment(Qt.AlignLeft | Qt.AlignLeft)

        self.controlsLayout.addWidget(self.text_widget)
        self.controlsLayout.addWidget(self.result_widget)


        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.returnPressed.connect(self.update_display)

        # Adding Completer.
        # self.completer = QCompleter(widget_names)
        # self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.searchbar.setCompleter(self.completer)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Control Panel')


    def update_display(self):
        if(self.finalYaer == '' or self.word != self.searchbar.text()):
            # pt = wikipedia.page(self.searchbar.text())
            self.word = self.searchbar.text()
            wiki_page = getWikiText(self.word)
            text = wiki_page[0] 
            self.title = wiki_page[1]
            self.text_widget.setText(text[0:300])
            self.finalYaer = yearFinder(text)
            self.result_widget.setText(self.finalYaer)
        else:
                file1 = open("/home/khashayar/notess/notes/EX/presocratics.md", "a")
                file1.write(f'| {self.title} | {self.finalYaer} |\n')
                file1.close()
                self.searchbar.setText("")
                self.text_widget.setText("")
                self.result_widget.setText("")
                self.finalYaer = ''


app = QApplication(sys.argv)
w = MainWindow()
w.resize(600, 200)
w.show()
sys.exit(app.exec_())
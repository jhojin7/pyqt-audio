# main.py
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsLineItem,
    QLabel, QWidget, QTextEdit,)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from audio import AudioManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_manager = AudioManager()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout
        layout = QVBoxLayout()

        # Create a QGraphicsView for waveform display
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Add a label for additional information
        self.info_label = QLabel("Audio Player")
        layout.addWidget(self.info_label)

        # Add a QTextEdit for additional information
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        # Connect text edit to autosave method
        self.text_edit.textChanged.connect(self.autosave_text)

        central_widget.setLayout(layout)

        # Connect file menu actions to methods
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        self.action_open = self.file_menu.addAction('Open Folder')
        self.action_open.triggered.connect(self.open_folder_dialog)

        # Set up keyboard shortcuts
        self.shortcut_play_pause = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.shortcut_play_pause.activated.connect(
            self.audio_manager.toggle_play_pause)
        # self.audio_manager.pause_audio)

        self.shortcut_next_audio = QShortcut(QKeySequence(Qt.Key_N), self)
        self.shortcut_next_audio.activated.connect(
            self.audio_manager.next_audio)

        self.shortcut_previous_audio = QShortcut(QKeySequence(Qt.Key_P), self)
        self.shortcut_previous_audio.activated.connect(
            self.audio_manager.previous_audio)

        self.shortcut_speed_up = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut_speed_up.activated.connect(
            lambda: self.audio_manager.adjust_speed(0.1))

        self.shortcut_speed_down = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut_speed_down.activated.connect(
            lambda: self.audio_manager.adjust_speed(-0.1))

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            audio_files = [file for file in os.listdir(
                folder_path) if file.endswith(('.mp3', '.wav'))]
            if audio_files:
                selected_file = os.path.join(folder_path, audio_files[0])
                self.audio_manager.play_audio(selected_file)

    def autosave_text(self):
        # Autosave text to a file with the same name as the audio file
        # if self.audio_manager.player.state() == QMediaPlayer.PlayingState:
        audio_file_path = self.audio_manager.player.currentMedia().canonicalUrl().toLocalFile()
        text_file_path = os.path.splitext(audio_file_path)[0] + ".txt"
        with open(text_file_path, 'w') as file:
            file.write(self.text_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

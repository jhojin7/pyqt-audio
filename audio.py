# audio.py
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class AudioManager:
    def __init__(self):
        self.player = QMediaPlayer()

    def toggle_play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def play_audio(self, file_path):
        content = QMediaContent(QUrl.fromLocalFile(file_path))
        self.player.setMedia(content)
        self.player.play()

    def pause_audio(self):
        self.player.pause()

    def next_audio(self):
        # Implement logic to play the next audio file
        pass

    def previous_audio(self):
        # Implement logic to play the previous audio file
        pass

    def adjust_speed(self, factor):
        current_speed = self.player.playbackRate()
        print(current_speed)
        self.player.setPlaybackRate(current_speed+factor)

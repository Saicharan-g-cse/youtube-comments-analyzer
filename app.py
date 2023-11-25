import sys

from youtube import YouTube
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QTextEdit, QWidget


class YouTubeCommentsAnalyzer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.paint_ui_components()

    def paint_ui_components(self):
        self.setWindowTitle('YouTube Comments Analyzer')
        self.setGeometry(100, 100, 600, 400)

        # API key and video ID input widgets
        self.api_key_label = QLabel('YouTube API Key:')
        self.api_key_input = QTextEdit(self)
        self.video_id_label = QLabel('YouTube Video ID:')
        self.video_id_input = QTextEdit(self)

        # Output labels
        self.result_label = QLabel('Results:')
        self.result_output = QLabel(self)

        # Analyze button
        self.analyze_button = QPushButton('Analyze Comments', self)
        self.analyze_button.clicked.connect(self.analyze_comments)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(self.video_id_label)
        layout.addWidget(self.video_id_input)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def analyze_comments(self):
        api_key = self.api_key_input.toPlainText().strip()
        video_id = self.video_id_input.toPlainText().strip()

        youtube = YouTube(api_key)
        comments = youtube.get_video_comments(part="snippet", videoId=video_id, textFormat="plainText")
        print(len(comments))
        print(comments)
        analyzer = youtube.get_comment_feelings(comments)

        self.result_output.setText(f"Positive: {analyzer['Positive']}\tNegative: {analyzer['Negative']}")


def main():
    app = QApplication(sys.argv)
    analyzer = YouTubeCommentsAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

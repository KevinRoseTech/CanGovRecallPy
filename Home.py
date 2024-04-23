import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

class RecallWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.setWindowTitle("Recall Search")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()

        # Input for recall ID
        self.recall_id_input = QLineEdit(self)
        self.recall_id_input.setPlaceholderText("Enter recall ID")
        self.layout.addWidget(self.recall_id_input)

        # Button for searching
        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.layout.addWidget(self.search_button)

        # Text edit for displaying results
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        self.layout.addWidget(self.results_text)

        self.central_widget.setLayout(self.layout)

    def on_search_clicked(self):
        recall_id = self.recall_id_input.text()
        self.fetch_recall_details(recall_id)

    def fetch_recall_details(self, recall_id):
        url = f"http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/{recall_id}/en"
        response = requests.get(url)
        if response.status_code == 200:
            recall_data = response.json()
            self.display_recall_details(recall_data)
        else:
            self.results_text.setText("Failed to fetch recall details.")

    def display_recall_details(self, recall_data):
        details = (
            f"URL: {recall_data.get('url')}\n"
            f"Recall ID: {recall_data.get('recallId')}\n"
            f"Title: {recall_data.get('title').strip()}\n"
            f"Start Date: {recall_data.get('start_date')}\n"
            f"Date Published: {recall_data.get('date_published')}\n"
            f"Category: {', '.join(str(cat) for cat in recall_data.get('category', []))}\n"
        )
        self.results_text.setText(details)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RecallWindow()
    win.show()
    sys.exit(app.exec_())

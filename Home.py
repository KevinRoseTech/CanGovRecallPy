# https://github.com/KevinRoseTech/CanGovRecallPy
import sys
import requests
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, \
    QTabWidget, QListWidget, QMessageBox


class RecallWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recall Grabber")
        self.setGeometry(100, 100, 800, 600)

        #MySQL connection settings
        self.db = mysql.connector.connect(
            host="localhost",
            user="savedacc",
            password="example",
            database="recalls"
        )
        self.cursor = self.db.cursor()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        #Tab 1: Search recalls
        self.search_tab = QWidget()
        self.setup_search_tab()
        #Tab 2: Saved recalls
        self.saved_tab = QWidget()
        self.setup_saved_tab()
        self.tab_widget.addTab(self.search_tab, "Home")
        self.tab_widget.addTab(self.saved_tab, "Saved")

    def setup_search_tab(self):
        layout = QVBoxLayout()

        self.recall_id_input = QLineEdit()
        self.recall_id_input.setPlaceholderText("Enter recall ID")
        layout.addWidget(self.recall_id_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.save_button = QPushButton("Save Recall")
        self.save_button.clicked.connect(self.on_save_clicked)
        layout.addWidget(self.save_button)

        self.search_tab.setLayout(layout)

    def setup_saved_tab(self):
        layout = QVBoxLayout()
        self.saved_list = QListWidget()
        self.load_saved_recalls()
        layout.addWidget(self.saved_list)
        self.saved_tab.setLayout(layout)
        self.saved_list.itemClicked.connect(self.display_saved_recall_details)

    def display_saved_recall_details(self, item):
        recall_id = item.text().split(': ')[0]
        query = "SELECT * FROM saved_recalls WHERE recall_id = %s"
        try:
            self.cursor.execute(query, (recall_id,))
            recall = self.cursor.fetchone()
            if recall:
                details = f"""
                Recall ID: {recall[0]}
                Title: {recall[1]}
                Start Date: {recall[2]}
                Date Published: {recall[3]}
                Category: {recall[4]}
                URL: {recall[5]}
                """
                QMessageBox.information(self, "Recall Details", details)
            else:
                QMessageBox.information(self, "Not Found", "No details found for the selected recall.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred when accessing the database: {str(e)}")

    def on_search_clicked(self):
        recall_id = self.recall_id_input.text().strip()
        self.fetch_recall_details(recall_id)

    def fetch_recall_details(self, recall_id):
        try:
            url = f"http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/{recall_id}/en"
            response = requests.get(url, timeout=10)  #EH: timeout request in case it hangs endlessly
            if response.status_code == 200:
                try:
                    self.current_recall = response.json()
                    self.display_recall_details(self.current_recall)
                except ValueError as e:  #EH: Catches JSON decode errors
                    self.results_text.setText("Error processing the API response. Please try again later.")
                    print(f"JSON Error: {e}")  #EH: Logs to debug
            elif response.status_code == 404:
                self.results_text.setText("Recall ID not found. Please check the ID and try again.")
            else:
                self.results_text.setText(
                    f"Unexpected response status: {response.status_code}. Please try again later.")
        except requests.exceptions.RequestException as e:
            self.results_text.setText(f"Network error: {str(e)}")
            print(f"Request Exception: {e}")  #EH: Logs to console
        except Exception as e:
            self.results_text.setText("An unexpected error occurred. Please contact support if the problem persists.")
            print(f"General Exception: {e}")  #EH: Logs to console

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

    def on_save_clicked(self):
        if self.current_recall:
            try:
                query = "INSERT INTO saved_recalls (recall_id, title, start_date, date_published, category, url) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (
                    self.current_recall['recallId'],
                    self.current_recall['title'].strip(),
                    self.current_recall['start_date'],
                    self.current_recall['date_published'],
                    ', '.join(str(cat) for cat in self.current_recall.get('category', [])),
                    self.current_recall['url']
                )
                self.cursor.execute(query, values)
                self.db.commit()
                self.load_saved_recalls()
                QMessageBox.information(self, "Saved", "Recall has been saved successfully!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error saving to database: {str(e)}")
                self.db.rollback()

    def load_saved_recalls(self):
        try:
            self.cursor.execute("SELECT recall_id, title FROM saved_recalls")
            self.saved_list.clear()
            for (recall_id, title) in self.cursor:
                self.saved_list.addItem(
                    f"{recall_id}: {title}")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading saved recalls: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RecallWindow()
    mainWin.show()
    sys.exit(app.exec_())

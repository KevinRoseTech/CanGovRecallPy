import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Home import Ui_MainWindow  # Import the UI class
from API import RecallsAPI  # Make sure API.py is in the same directory or in the Python path
from RecallTile import RecallTile  # Import the custom widget



class GUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)
        # Connect the button click and return pressed to perform_search method
        self.pushButton.clicked.connect(self.perform_search)
        self.lineEdit_4.returnPressed.connect(self.perform_search)

    def perform_search(self):
        recall_id = self.lineEdit_4.text().strip()
        if recall_id:
            try:
                result = RecallsAPI.get_recall_details(recall_id)  # Make sure this function is defined in your API module
                self.display_details(result)
            except Exception as e:
                print(f"Error during search: {str(e)}")
                QMessageBox.critical(self, "Search Error", "Failed to fetch recall details.")
                self.textEdit.setText("Failed to load recall details.")
        else:
            QMessageBox.information(self, "Input Error", "Please enter a valid Recall ID.")

    def display_details(self, recall_details):
        if recall_details and 'recallId' in recall_details:
            details_text = f"Recall ID: {recall_details['recallId']}\nTitle: {recall_details['title']}\n"
            details_text += f"Category: {', '.join(recall_details.get('category', []))}\n"
            details_text += f"Published Date: {recall_details['date_published']}\nURL: {recall_details['url']}\n\n"
            for panel in recall_details.get('panels', []):
                details_text += f"{panel['title']}:\n{panel['text']}\n\n"
            self.textEdit.setText(details_text)
        else:
            self.textEdit.setText("No details found or invalid recall ID.")

def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

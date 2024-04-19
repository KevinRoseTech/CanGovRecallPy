import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Home import Ui_MainWindow  # Import the UI class
from API import RecallsAPI  # Make sure API.py is in the same directory or in the Python path
from RecallTile import RecallTile  # Import the custom widget



class GUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)
        # Connect your line edits or a new submit button to searchRecalls
        # Assuming you want to trigger the search when the user presses Enter in any QLineEdit
        self.lineEdit_2.returnPressed.connect(self.searchRecalls)
        self.lineEdit_5.returnPressed.connect(self.searchRecalls)
        self.lineEdit.returnPressed.connect(self.searchRecalls)
        self.lineEdit_4.returnPressed.connect(self.searchRecalls)
        self.lineEdit_3.returnPressed.connect(self.searchRecalls)

    def searchRecalls(self):
        # Assuming the search API returns a list of dictionaries
        results = RecallsAPI.search_recalls(
            self.lineEdit_2.text(),
            category=self.lineEdit.text(),
            department=self.lineEdit_5.text(),
            date=self.lineEdit_4.text(),
            last_updated=self.lineEdit_3.text()
        )

        self.display_search_results(results)

    def display_search_results(self, search_results):
        # Clear existing widgets from the grid layout
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Populate the grid layout with new tiles
        row, col = 0, 0
        for recall in search_results:
            tile = RecallTile(recall)
            self.gridLayout.addWidget(tile, row, col)
            col += 1
            if col >= 3:  # Assuming you want 3 columns
                col = 0
                row += 1
def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

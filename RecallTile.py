from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class RecallTile(QWidget):
    def __init__(self, recall_data, parent=None):
        super(RecallTile, self).__init__(parent)
        layout = QVBoxLayout(self)

        title = QLabel(recall_data.get('title', 'No Title'))
        department = QLabel(f"Department: {recall_data.get('department', 'N/A')}")
        category = QLabel(f"Category: {recall_data.get('category', ['N/A'])[0]}")
        date_published = QLabel(f"Date Published: {recall_data.get('date_published', 'N/A')}")

        layout.addWidget(title)
        layout.addWidget(department)
        layout.addWidget(category)
        layout.addWidget(date_published)

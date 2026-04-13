import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox, QHeaderView)


#functions:
class Student:
    def __init__(self, name):
        if not name or name.isnumeric():
            raise ValueError("Le nom ne peut pas être vide ou un nombre.")
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        if grade < 0 or grade > 20:
            raise ValueError("La note doit être entre 0 et 20.")
        self.grades.append(grade)

    @property
    def average(self):
        if not self.grades: return 0
        return sum(self.grades) / len(self.grades)


#main window;
class StudentManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.students = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Système de Gestion des Notes")
        self.resize(800, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)


        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom de l'étudiant")
        self.grades_input = QLineEdit()
        self.grades_input.setPlaceholderText("6 notes séparées par des espaces (ex: 12 14 10...)")

        add_btn = QPushButton("Ajouter Étudiant")
        add_btn.clicked.connect(self.add_student)

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.grades_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)


        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Nom", "M1", "M2", "M3", "M4", "M5", "M6", "Moyenne"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

#buttons:
        btn_layout = QHBoxLayout()

        sort_btn = QPushButton("Trier par Moyenne")
        sort_btn.clicked.connect(self.sort_and_refresh)

        clear_btn = QPushButton("Effacer Tout")
        clear_btn.clicked.connect(self.clear_table)

        btn_layout.addWidget(sort_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

    def add_student(self):
        name = self.name_input.text()
        grades_text = self.grades_input.text().split()

        try:
            if len(grades_text) != 6:
                raise ValueError("Veuillez entrer exactement 6 notes.")

            new_student = Student(name)
            for g in grades_text:
                new_student.add_grade(float(g))

            self.students.append(new_student)
            self.refresh_table()


            self.name_input.clear()
            self.grades_input.clear()

        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def refresh_table(self):
        self.table.setRowCount(0)
        for student in self.students:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(student.name))
            for i, grade in enumerate(student.grades):
                self.table.setItem(row, i + 1, QTableWidgetItem(f"{grade:.2f}"))

            avg_item = QTableWidgetItem(f"{student.average:.2f}")
            self.table.setItem(row, 7, avg_item)

    def sort_and_refresh(self):
        self.students.sort(key=lambda s: s.average, reverse=True)
        self.refresh_table()

    def clear_table(self):
        self.students = []
        self.table.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagerGUI()
    window.show()
    sys.exit(app.exec())
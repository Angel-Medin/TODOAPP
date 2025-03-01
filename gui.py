from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QLabel, QMenu, QInputDialog, QHeaderView
from PyQt5.QtCore import QPoint, Qt

class ToDoApp(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("To Do List")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        self.layout = QVBoxLayout()

        # Tabla con 5 columnas: Tarea, Descripción, Estado, Menú y una columna oculta para el ID
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tarea", "Descripción", "Estado", "Menú", "ID"])
        # Ajustar la columna del menú al contenido
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table)

        # Sección para agregar nuevas tareas
        self.input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Nueva tarea")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descripción")
        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.add_task)

        self.input_layout.addWidget(QLabel("Tarea:"))
        self.input_layout.addWidget(self.task_input)
        self.input_layout.addWidget(QLabel("Descripción:"))
        self.input_layout.addWidget(self.desc_input)
        self.input_layout.addWidget(self.add_button)
        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)
        self.load_task()

    def load_task(self):
        """Carga las tareas de la base de datos en la tabla."""
        self.table.setRowCount(0)
        tasks = self.db_manager.get_all_tasks()

        for task_id, task, desc, status in tasks:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(task))
            self.table.setItem(row_position, 1, QTableWidgetItem(desc))
            self.table.setItem(row_position, 2, QTableWidgetItem(status))

            # Botón de menú contextual en la columna 3
            menu_button = QPushButton(":")
            menu_button.setContextMenuPolicy(Qt.CustomContextMenu)
            menu_button.customContextMenuRequested.connect(lambda pos, r=row_position: self.show_menu(r))
            self.table.setCellWidget(row_position, 3, menu_button)

            # Columna oculta para almacenar el ID de la tarea (columna 4)
            self.table.setItem(row_position, 4, QTableWidgetItem(str(task_id)))
            self.table.hideColumn(4)

    def add_task(self):
        """Agrega una nueva tarea con estado 'Pendiente' por defecto."""
        task = self.task_input.text().strip()
        desc = self.desc_input.text().strip()

        if task and desc:
            self.db_manager.add_task(task, desc, status='Pendiente')
            self.load_task()
            self.task_input.clear()
            self.desc_input.clear()

    def show_menu(self, row):
        """Muestra el menú contextual para editar, eliminar o actualizar el estado de la tarea."""
        menu = QMenu()
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Eliminar")
        finish_action = menu.addAction("Finalizado")
        pending_action = menu.addAction("Marcar como Pendiente")
        in_progress_action = menu.addAction("Marcar como En Curso")

        button = self.table.cellWidget(row, 3)
        global_pos = button.mapToGlobal(QPoint(0, button.height()))
        action = menu.exec_(global_pos)

        # Obtener el ID de la tarea desde la columna oculta (índice 4)
        task_id = int(self.table.item(row, 4).text())

        if action == edit_action:
            self.edit_task(row, task_id)
        elif action == delete_action:
            self.delete_task(row, task_id)
        elif action == finish_action:
            self.update_status(row, task_id, "Finalizado")
        elif action == pending_action:
            self.update_status(row, task_id, "Pendiente")
        elif action == in_progress_action:
            self.update_status(row, task_id, "En Curso")

    def edit_task(self, row, task_id):
        """Abre diálogos para editar la tarea, descripción y estado."""
        old_task = self.table.item(row, 0).text()
        old_desc = self.table.item(row, 1).text()
        old_status = self.table.item(row, 2).text()

        new_task, ok_task = QInputDialog.getText(self, "Editar Tarea", "Nueva tarea:", text=old_task)
        if not ok_task or not new_task.strip():
            return

        new_desc, ok_desc = QInputDialog.getText(self, "Editar Descripción", "Nueva descripción:", text=old_desc)
        if not ok_desc or not new_desc.strip():
            return

        new_status, ok_status = QInputDialog.getItem(
            self,
            "Seleccionar Estado",
            "Estado:",
            ["Pendiente", "En Curso", "Finalizado"],
            current=0 if old_status == "Pendiente" else 1 if old_status == "En Curso" else 2
        )
        if not ok_status:
            return

        self.db_manager.update_task(task_id, new_task, new_desc, new_status)
        self.load_task()

    def update_status(self, row, task_id, new_status):
        """Actualiza el estado de la tarea manteniendo los otros campos."""
        current_task = self.table.item(row, 0).text()
        current_desc = self.table.item(row, 1).text()
        self.db_manager.update_task(task_id, current_task, current_desc, new_status)
        self.load_task()

    def delete_task(self, row, task_id):
        """Elimina la tarea seleccionada."""
        self.db_manager.delete_task(task_id)
        self.load_task()

def apply_styles(widget):
    style_sheet = """
    /* Estilo general para todos los widgets */
    QWidget {
        background-color: #2E2E2E;
        color: #F0F0F0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Estilos para la tabla */
    QTableWidget {
        background-color: #3C3F41;
        gridline-color: #6C6C6C;
    }
    QHeaderView::section {
        background-color: #3C3F41;
        color: #F0F0F0;
        padding: 4px;
        border: 1px solid #6C6C6C;
    }
    /* Estilos para botones */
    QPushButton {
        background-color: #4A90E2;
        border: none;
        padding: 5px 10px;
        color: #FFFFFF;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #357ABD;
    }
    /* Estilos para QLineEdit */
    QLineEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 4px;
    }
    /* Estilos para los menús */
    QMenu {
        background-color: #3C3F41;
        color: #F0F0F0;
        border: 1px solid #6C6C6C;
    }
    QMenu::item:selected {
        background-color: #4A90E2;
    }
    """
    widget.setStyleSheet(style_sheet)

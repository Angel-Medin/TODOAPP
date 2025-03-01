import sqlite3

class DatabaseManager:
    def __init__(self, db_name = "tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """Cra la tabla 'tasks' si no existe"""
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS tasks(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task TEXT NOT NULL,
                            description TEXT NOT NULL,
                            status TEXT DEFAULT 'Pendiente' NOT NULL
                            )
                        
                        """)
        self.conn.commit()
        

    def add_task(self, task, description, status = 'Pendiente'):
        """Inserta una nueva tarea en la base de datos"""
        self.cursor.execute("INSERT INTO tasks (task, description, status) VALUES (?,?,?)", (task, description, status))
        self.conn.commit()


    def get_all_tasks(self):
        """Obtiene todas las tareas de la base de datos"""
        self.cursor.execute("SELECT id, task, description, status FROM tasks")
        return self.cursor.fetchall()
    

    def update_task(self, task_id, new_task, new_description, new_status):
        """Actualiza una tarea por su ID"""
        self.cursor.execute("""UPDATE tasks
                            SET task = ?,
                                description = ?,
                                status = ?
                                WHERE id = ?
                            """, (new_task, new_description, new_status, task_id))
        self.conn.commit()


    def delete_task(self, task_id):
        """Elimina una tarea por su nombre"""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()


    def close(self):
        """Cierra la conexion a la base de datos"""
        self.conn.close()
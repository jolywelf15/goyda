import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root', 
            'password': 'Windowsxp34',  # ЗАМЕНИТЕ НА ВАШ ПАРОЛЬ
            'port': 3306
        }
        self.database_name = 'smartphone_assembly'
        self.init_database()
    
    def get_connection(self, use_database=True):
        try:
            config = self.db_config.copy()
            if use_database:
                config['database'] = self.database_name
            return mysql.connector.connect(**config)
        except Error as e:
            print(f"❌ Ошибка подключения к MySQL: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        """Выполнение запроса для MySQL"""
        conn = self.get_connection()
        if conn is None:
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
                conn.commit()
                
            cursor.close()
            conn.close()
            return result
            
        except Error as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            conn.rollback()
            cursor.close()
            conn.close()
            return None
    
    def init_database(self):
        """Инициализация базы данных MySQL"""
        try:
            # Сначала создаем/проверяем базу данных
            conn = self.get_connection(use_database=False)
            if conn is None:
                return
                
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            cursor.execute(f"USE {self.database_name}")
            print(f"✅ База данных {self.database_name} создана/выбрана")
            
            # Отключаем проверку внешних ключей для создания таблиц
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Таблица сотрудников (первая, так как на неё ссылаются другие)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    position VARCHAR(50)
                )
            ''')
            print("✅ Таблица employees создана")
            
            # Таблица моделей смартфонов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS smartphone_models (
                    model_id INT AUTO_INCREMENT PRIMARY KEY,
                    model_name VARCHAR(100) NOT NULL
                )
            ''')
            print("✅ Таблица smartphone_models создана")
            
            # Таблица комплектующих
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS components (
                    component_id INT AUTO_INCREMENT PRIMARY KEY,
                    component_name VARCHAR(100) NOT NULL,
                    unit VARCHAR(50),
                    expiry_date DATE,
                    quantity INT DEFAULT 0,
                    last_update DATE
                )
            ''')
            print("✅ Таблица components создана")
            
            # Таблица бригад
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    team_id INT AUTO_INCREMENT PRIMARY KEY,
                    team_name VARCHAR(100) NOT NULL,
                    order_id INT
                )
            ''')
            print("✅ Таблица teams создана")
            
            # Таблица состава бригад
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    team_id INT,
                    employee_id INT,
                    PRIMARY KEY (team_id, employee_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id),
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                )
            ''')
            print("✅ Таблица team_members создана")
            
            # Таблица производственных заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assembly_orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY,
                    model_id INT,
                    quantity INT NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    week_number INT,
                    team_id INT,
                    status VARCHAR(20) DEFAULT 'В работе',
                    FOREIGN KEY (model_id) REFERENCES smartphone_models(model_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                )
            ''')
            print("✅ Таблица assembly_orders создана")
            
            # Таблица состава моделей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_components (
                    model_id INT,
                    component_id INT,
                    quantity INT NOT NULL,
                    PRIMARY KEY (model_id, component_id),
                    FOREIGN KEY (model_id) REFERENCES smartphone_models(model_id),
                    FOREIGN KEY (component_id) REFERENCES components(component_id)
                )
            ''')
            print("✅ Таблица model_components создана")
            
            # Таблица отчетов по заказам
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_reports (
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    model_id INT,
                    assembled_units INT,
                    defect_quantity INT,
                    time_spent INT,
                    report_date DATE,
                    team_id INT,
                    FOREIGN KEY (order_id) REFERENCES assembly_orders(order_id),
                    FOREIGN KEY (model_id) REFERENCES smartphone_models(model_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                )
            ''')
            print("✅ Таблица order_reports создана")
            
            # Включаем обратно проверку внешних ключей
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("🎉 Все таблицы созданы успешно!")
            
        except Error as e:
            print(f"❌ Ошибка инициализации MySQL: {e}")
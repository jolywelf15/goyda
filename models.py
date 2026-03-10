import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class SmartphoneAssemblySystem:
    def __init__(self):
        # Конфигурация для XAMPP (пустой пароль)
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # ПУСТОЙ пароль для XAMPP
            'port': 3306
        }
        self.database_name = 'smartphone_assembly'
        self.conn = None
        self.create_database()  # Создаем базу если нет
        self.connect()          # Подключаемся к базе
        self.create_tables()    # Создаем таблицы
    
    def create_database(self):
        """Создает базу данных если она не существует"""
        try:
            # Подключаемся к серверу без указания базы данных
            temp_conn = mysql.connector.connect(**self.db_config)
            cursor = temp_conn.cursor()
            
            # Создаем базу данных если ее нет
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            print(f"✅ База данных '{self.database_name}' создана/существует")
            
            cursor.close()
            temp_conn.close()
            
        except Error as e:
            print(f"❌ Ошибка создания базы данных: {e}")
    
    def connect(self):
        """Создает соединение с базой данных MySQL"""
        try:
            # Добавляем имя базы данных в конфигурацию
            config_with_db = self.db_config.copy()
            config_with_db['database'] = self.database_name
            
            self.conn = mysql.connector.connect(**config_with_db)
            print(f"✅ Подключение к базе данных '{self.database_name}' успешно!")
        except Error as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            self.conn = None
    
    def reconnect(self):
        """Переподключение к базе данных"""
        if self.conn:
            self.conn.close()
        self.connect()
    
    def execute_query(self, query, params=None, fetch=False, fetch_one=False):
        """Выполняет SQL-запрос"""
        # Переподключаемся если соединение потеряно
        if not self.conn or not self.conn.is_connected():
            print("🔄 Переподключение к базе данных...")
            self.reconnect()
            if not self.conn:
                print("❌ Не удалось переподключиться к базе данных")
                return None
        
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            elif fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.lastrowid
                self.conn.commit()
            
            cursor.close()
            return result
            
        except Error as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            print(f"Запрос: {query}")
            print(f"Параметры: {params}")
            if self.conn:
                self.conn.rollback()
            cursor.close()
            return None
    
    def create_tables(self):
        """Создает таблицы в базе данных"""
        if not self.conn:
            print("❌ Нет соединения с базой данных")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Отключаем проверку внешних ключей для создания таблиц
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            #ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблица 'users' создана")
            
            # Таблица комплектующих
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS components (
                    component_id INT AUTO_INCREMENT PRIMARY KEY,
                    component_name VARCHAR(100) NOT NULL,
                    unit VARCHAR(50),
                    quantity INT DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблица 'components' создана")
            
            # Таблица моделей смартфонов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS smartphone_models (
                    model_id INT AUTO_INCREMENT PRIMARY KEY,
                    model_name VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблица 'smartphone_models' создана")
            
            # Таблица сотрудников
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    position VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблица 'employees' создана")
            
            # Таблица бригад
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    team_id INT AUTO_INCREMENT PRIMARY KEY,
                    team_name VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблица 'teams' создана")
            
            # Таблица связи сотрудников и бригад
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    team_id INT,
                    employee_id INT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (team_id, employee_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
                )
            ''')
            print("✅ Таблица 'team_members' создана")
            
            # Таблица заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assembly_orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY,
                    model_id INT NOT NULL,
                    quantity INT NOT NULL,
                    team_id INT NOT NULL,
                    start_date DATE DEFAULT (CURRENT_DATE),
                    end_date DATE,
                    status VARCHAR(20) DEFAULT 'В работе',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (model_id) REFERENCES smartphone_models(model_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                )
            ''')
            print("✅ Таблица 'assembly_orders' создана")
            
            # Таблица отчетов о сборке
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_reports (
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    model_id INT NOT NULL,
                    assembled_units INT NOT NULL,
                    defect_quantity INT DEFAULT 0,
                    time_spent INT NOT NULL,
                    report_date DATE DEFAULT (CURRENT_DATE),
                    team_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES assembly_orders(order_id),
                    FOREIGN KEY (model_id) REFERENCES smartphone_models(model_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                )
            ''')
            print("✅ Таблица 'order_reports' создана")
            
            # Включаем обратно проверку внешних ключей
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            self.conn.commit()
            cursor.close()
            print("🎉 Все таблицы созданы успешно!")
            
            # Создаем администратора по умолчанию если таблица пользователей пустая
            self.create_default_user()
            
        except Error as e:
            print(f"❌ Ошибка создания таблиц: {e}")
    
    def create_default_user(self):
        """Создает пользователя по умолчанию с паролем 1234"""
        try:
            query = "SELECT COUNT(*) as count FROM users"
            result = self.execute_query(query, fetch_one=True)
            
            if result and result['count'] == 0:
                query = """
                    INSERT INTO users (username, password, full_name, role) 
                    VALUES (%s, %s, %s, %s)
                """
                self.execute_query(query, ('admin', 'admin123', 'Администратор', 'admin'))
                print("👤 Тестовый пользователь создан (логин: admin, пароль: admin123)")
                
        except Error as e:
            print(f"❌ Ошибка создания пользователя: {e}")
    
     #МЕТОДЫ АВТОРИЗАЦИИ 
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        query = """
            SELECT user_id, username, full_name, role 
            FROM users 
            WHERE username = %s AND password = %s
        """
        result = self.execute_query(query, (username, password), fetch_one=True)
        return result if result else None
    
    def add_user(self, username, password, full_name, role='user'):
        """Добавление нового пользователя"""
        query = """
            INSERT INTO users (username, password, full_name, role) 
            VALUES (%s, %s, %s, %s)
        """
        result = self.execute_query(query, (username, password, full_name, role))
        return result is not None
    
    def get_users(self):
        """Получение списка всех пользователей"""
        query = "SELECT user_id, username, full_name, role, created_at FROM users ORDER BY user_id"
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_user(self, user_id):
        """Удаление пользователя"""
        # Нельзя удалить администратора по умолчанию
        if user_id == 1:
            return False
        
        query = "DELETE FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,))
        return result is not None
    
    def update_user(self, user_id, username, full_name, role):
        """Обновление данных пользователя"""
        query = """
            UPDATE users 
            SET username = %s, full_name = %s, role = %s 
            WHERE user_id = %s
        """
        result = self.execute_query(query, (username, full_name, role, user_id))
        return result is not None
    
    def change_password(self, user_id, new_password):
        """Изменение пароля пользователя"""
        query = "UPDATE users SET password = %s WHERE user_id = %s"
        result = self.execute_query(query, (new_password, user_id))
        return result is not None
    
    def user_exists(self, username):
        """Проверяет, существует ли пользователь с таким логином"""
        query = "SELECT user_id FROM users WHERE username = %s"
        result = self.execute_query(query, (username,), fetch_one=True)
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ КОМПЛЕКТУЮЩИХ ==========
    
    def add_component(self, name, unit=None, quantity=0):
        """Добавляет комплектующее на склад"""
        query = """
            INSERT INTO components (component_name, unit, quantity) 
            VALUES (%s, %s, %s)
        """
        result = self.execute_query(query, (name, unit, quantity))
        return result is not None
    
    def get_components(self):
        """Возвращает список всех комплектующих"""
        query = "SELECT * FROM components ORDER BY component_id"
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def update_component(self, component_id, quantity):
        """Обновляет количество комплектующих"""
        query = "UPDATE components SET quantity = %s WHERE component_id = %s"
        result = self.execute_query(query, (quantity, component_id))
        return result is not None
    
    def delete_component(self, component_id):
        """Удаляет комплектующее по ID"""
        query = "DELETE FROM components WHERE component_id = %s"
        result = self.execute_query(query, (component_id,))
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ МОДЕЛЕЙ СМАРТФОНОВ ==========
    
    def add_model(self, name):
        """Добавляет модель смартфона"""
        query = "INSERT INTO smartphone_models (model_name) VALUES (%s)"
        result = self.execute_query(query, (name,))
        return result is not None
    
    def get_models(self):
        """Возвращает список всех моделей смартфонов"""
        query = "SELECT * FROM smartphone_models ORDER BY model_id"
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_model(self, model_id):
        """Удаляет модель по ID"""
        query = "DELETE FROM smartphone_models WHERE model_id = %s"
        result = self.execute_query(query, (model_id,))
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ СОТРУДНИКОВ ==========
    
    def add_employee(self, full_name, position=None):
        """Добавляет сотрудника"""
        query = "INSERT INTO employees (full_name, position) VALUES (%s, %s)"
        result = self.execute_query(query, (full_name, position))
        return result is not None
    
    def get_employees(self):
        """Возвращает список всех сотрудников"""
        query = "SELECT * FROM employees ORDER BY employee_id"
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_employee(self, employee_id):
        """Удаляет сотрудника по ID"""
        query = "DELETE FROM employees WHERE employee_id = %s"
        result = self.execute_query(query, (employee_id,))
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ БРИГАД ==========
    
    def add_team(self, team_name):
        """Добавляет бригаду"""
        query = "INSERT INTO teams (team_name) VALUES (%s)"
        result = self.execute_query(query, (team_name,))
        return result is not None
    
    def get_teams(self):
        """Возвращает список всех бригад"""
        query = "SELECT * FROM teams ORDER BY team_id"
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_team(self, team_id):
        """Удаляет бригаду по ID"""
        query = "DELETE FROM teams WHERE team_id = %s"
        result = self.execute_query(query, (team_id,))
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ УПРАВЛЕНИЯ СОСТАВОМ БРИГАД ==========
    
    def add_employee_to_team(self, team_id, employee_id):
        """Добавляет сотрудника в бригаду"""
        # Проверяем, не состоит ли уже сотрудник в этой бригаде
        check_query = "SELECT * FROM team_members WHERE team_id = %s AND employee_id = %s"
        existing = self.execute_query(check_query, (team_id, employee_id), fetch_one=True)
        
        if existing:
            return False  # Уже состоит в бригаде
        
        query = """
            INSERT INTO team_members (team_id, employee_id) 
            VALUES (%s, %s)
        """
        result = self.execute_query(query, (team_id, employee_id))
        return result is not None
    
    def remove_employee_from_team(self, team_id, employee_id):
        """Удаляет сотрудника из бригады"""
        query = "DELETE FROM team_members WHERE team_id = %s AND employee_id = %s"
        result = self.execute_query(query, (team_id, employee_id))
        return result is not None
    
    def get_team_members(self, team_id):
        """Возвращает список сотрудников в бригаде"""
        query = """
            SELECT e.employee_id, e.full_name, e.position 
            FROM employees e
            JOIN team_members tm ON e.employee_id = tm.employee_id
            WHERE tm.team_id = %s
            ORDER BY e.full_name
        """
        result = self.execute_query(query, (team_id,), fetch=True)
        return result if result else []
    
    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ЗАКАЗАМИ ==========
    
    def add_order(self, model_id, quantity, team_id, weeks=1):
        """Добавляет заказ на сборку"""
        # Проверяем, свободна ли бригада
        busy_check = """
            SELECT COUNT(*) as count 
            FROM assembly_orders 
            WHERE team_id = %s AND status = 'В работе'
        """
        busy_result = self.execute_query(busy_check, (team_id,), fetch_one=True)
        
        if busy_result and busy_result['count'] > 0:
            return False  # Бригада уже занята
        
        # Рассчитываем дату окончания
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(weeks=weeks)).strftime('%Y-%m-%d')
        
        query = """
            INSERT INTO assembly_orders 
            (model_id, quantity, team_id, start_date, end_date, status) 
            VALUES (%s, %s, %s, %s, %s, 'В работе')
        """
        result = self.execute_query(query, (model_id, quantity, team_id, start_date, end_date))
        return result is not None
    
    def get_orders(self):
        """Возвращает список всех заказов с дополнительной информацией"""
        query = """
            SELECT o.*, m.model_name, t.team_name
            FROM assembly_orders o
            JOIN smartphone_models m ON o.model_id = m.model_id
            JOIN teams t ON o.team_id = t.team_id
            ORDER BY o.order_id DESC
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def get_active_orders(self):
        """Возвращает только активные заказы"""
        query = """
            SELECT o.*, m.model_name, t.team_name
            FROM assembly_orders o
            JOIN smartphone_models m ON o.model_id = m.model_id
            JOIN teams t ON o.team_id = t.team_id
            WHERE o.status = 'В работе'
            ORDER BY o.end_date
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_order(self, order_id):
        """Удаляет заказ по ID"""
        query = "DELETE FROM assembly_orders WHERE order_id = %s"
        result = self.execute_query(query, (order_id,))
        return result is not None
    
    def get_busy_teams(self):
        """Возвращает список бригад, которые заняты в текущих заказах"""
        query = """
            SELECT DISTINCT t.team_id, t.team_name
            FROM teams t
            JOIN assembly_orders o ON t.team_id = o.team_id
            WHERE o.status = 'В работе'
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def complete_order(self, order_id):
        """Завершает заказ"""
        query = """
            UPDATE assembly_orders 
            SET status = 'Завершен', end_date = CURDATE()
            WHERE order_id = %s
        """
        result = self.execute_query(query, (order_id,))
        return result is not None
    
    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ОТЧЕТАМИ ==========
    
    def add_order_report(self, order_id, assembled_units, defect_quantity, time_spent):
        """Добавляет отчет о сборке"""
        # Проверяем, существует ли заказ
        order_check = self.execute_query(
            "SELECT order_id FROM assembly_orders WHERE order_id = %s",
            (order_id,), 
            fetch_one=True
        )
        
        if not order_check:
            print(f"❌ Заказ с ID {order_id} не найден")
            return False
        
        # Проверяем, не добавлен ли уже отчет для этого заказа
        report_check = self.execute_query(
            "SELECT report_id FROM order_reports WHERE order_id = %s",
            (order_id,), 
            fetch_one=True
        )
        
        if report_check:
            print(f"⚠️ Отчет для заказа {order_id} уже существует")
            return False
        
        # Получаем информацию о заказе для получения model_id и team_id
        order_info = self.execute_query(
            "SELECT model_id, team_id FROM assembly_orders WHERE order_id = %s",
            (order_id,), 
            fetch_one=True
        )
        
        if not order_info:
            return False
        
        query = """
            INSERT INTO order_reports 
            (order_id, model_id, assembled_units, defect_quantity, time_spent, team_id, report_date) 
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
        """
        result = self.execute_query(query, (
            order_id, 
            order_info['model_id'], 
            assembled_units, 
            defect_quantity, 
            time_spent,
            order_info['team_id']
        ))
        
        # Если отчет добавлен успешно, завершаем заказ
        if result:
            self.complete_order(order_id)
        
        return result
    
    def get_order_reports(self):
        """Возвращает список всех отчетов с дополнительной информацией"""
        query = """
            SELECT r.*, m.model_name, t.team_name, o.quantity as ordered_quantity
            FROM order_reports r
            JOIN assembly_orders o ON r.order_id = o.order_id
            JOIN smartphone_models m ON o.model_id = m.model_id
            JOIN teams t ON o.team_id = t.team_id
            ORDER BY r.report_id DESC
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def delete_report(self, report_id):
        """Удаляет отчет по ID"""
        query = "DELETE FROM order_reports WHERE report_id = %s"
        result = self.execute_query(query, (report_id,))
        return result is not None
    
    # ========== ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ==========
    
    def get_statistics(self):
        """Возвращает статистику по системе"""
        stats = {}
        
        try:
            # Количество комплектующих
            query = "SELECT COUNT(*) as count FROM components"
            result = self.execute_query(query, fetch_one=True)
            stats['components_count'] = result['count'] if result else 0
            
            # Общее количество комплектующих на складе
            query = "SELECT SUM(quantity) as total FROM components"
            result = self.execute_query(query, fetch_one=True)
            stats['components_total'] = result['total'] if result and result['total'] else 0
            
            # Количество моделей
            query = "SELECT COUNT(*) as count FROM smartphone_models"
            result = self.execute_query(query, fetch_one=True)
            stats['models_count'] = result['count'] if result else 0
            
            # Количество сотрудников
            query = "SELECT COUNT(*) as count FROM employees"
            result = self.execute_query(query, fetch_one=True)
            stats['employees_count'] = result['count'] if result else 0
            
            # Количество бригад
            query = "SELECT COUNT(*) as count FROM teams"
            result = self.execute_query(query, fetch_one=True)
            stats['teams_count'] = result['count'] if result else 0
            
            # Активные заказы
            query = "SELECT COUNT(*) as count FROM assembly_orders WHERE status = 'В работе'"
            result = self.execute_query(query, fetch_one=True)
            stats['active_orders'] = result['count'] if result else 0
            
            # Завершенные заказы
            query = "SELECT COUNT(*) as count FROM assembly_orders WHERE status = 'Завершен'"
            result = self.execute_query(query, fetch_one=True)
            stats['completed_orders'] = result['count'] if result else 0
            
            # Общее количество собранных единиц
            query = "SELECT SUM(assembled_units) as total FROM order_reports"
            result = self.execute_query(query, fetch_one=True)
            stats['total_assembled'] = result['total'] if result and result['total'] else 0
            
            # Общее количество брака
            query = "SELECT SUM(defect_quantity) as total FROM order_reports"
            result = self.execute_query(query, fetch_one=True)
            stats['total_defects'] = result['total'] if result and result['total'] else 0
            
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
        
        return stats
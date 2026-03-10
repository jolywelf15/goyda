import tkinter as tk
from tkinter import ttk, messagebox
from models import SmartphoneAssemblySystem

class SmartphoneAssemblyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Система сборки смартфонов")
        self.root.geometry("1200x700")
        
        self.system = SmartphoneAssemblySystem()
        
        # Инициализируем переменные для комбобоксов
        self.order_model = None
        self.order_team = None
        self.team_combo = None
        self.employee_combo = None
        self.order_combo = None
        self.report_order = None
        
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка просмотра данных
        self.view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_frame, text="Просмотр данных")
        
        # Вкладка добавления данных
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="Добавление данных")
        
        # Вкладка управления
        self.manage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_frame, text="Управление")
        
        self.create_view_tab()
        self.create_add_tab()
        self.create_manage_tab()
    
    def create_view_tab(self):
        # Фрейм для выбора типа данных
        view_selector_frame = ttk.Frame(self.view_frame)
        view_selector_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(view_selector_frame, text="Просмотр:").pack(side='left')
        
        self.view_var = tk.StringVar(value="components")
        view_types = [
            ("Комплектующие", "components"),
            ("Модели", "models"),
            ("Сотрудники", "employees"),
            ("Бригады", "teams"),
            ("Заказы", "orders"),
            ("Отчеты", "reports")
        ]
        
        for text, value in view_types:
            ttk.Radiobutton(view_selector_frame, text=text, variable=self.view_var, 
                           value=value, command=self.refresh_view).pack(side='left', padx=5)
        
        # Фрейм для таблицы и кнопки удаления
        table_frame = ttk.Frame(self.view_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Таблица для отображения данных
        self.tree = ttk.Treeview(table_frame)
        self.tree.pack(fill='both', expand=True, side='left')
        
        # Scrollbar для таблицы
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопка удаления выбранной записи
        delete_button = ttk.Button(self.view_frame, text="Удалить выбранное", 
                                 command=self.delete_selected)
        delete_button.pack(pady=5)
    
    def create_add_tab(self):
        # Фрейм для выбора типа добавляемых данных
        add_selector_frame = ttk.Frame(self.add_frame)
        add_selector_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_selector_frame, text="Добавить:").pack(side='left')
        
        self.add_var = tk.StringVar(value="component")
        add_types = [
            ("Комплектующее", "component"),
            ("Модель", "model"),
            ("Сотрудника", "employee"),
            ("Бригаду", "team"),
            ("Заказ", "order"),
            ("Отчет", "report")
        ]
        
        for text, value in add_types:
            ttk.Radiobutton(add_selector_frame, text=text, variable=self.add_var, 
                           value=value, command=self.show_add_form).pack(side='left', padx=5)
        
        # Фрейм для формы добавления
        self.add_form_frame = ttk.Frame(self.add_frame)
        self.add_form_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.show_add_form()
    
    def create_manage_tab(self):
        # Управление составом бригад
        team_manage_frame = ttk.LabelFrame(self.manage_frame, text="Управление составом бригад")
        team_manage_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(team_manage_frame, text="Бригада:").grid(row=0, column=0, padx=5, pady=5)
        self.team_combo = ttk.Combobox(team_manage_frame, state="readonly")
        self.team_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(team_manage_frame, text="Сотрудник:").grid(row=0, column=2, padx=5, pady=5)
        self.employee_combo = ttk.Combobox(team_manage_frame, state="readonly")
        self.employee_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(team_manage_frame, text="Добавить в бригаду", 
                  command=self.add_employee_to_team_gui).grid(row=0, column=4, padx=5, pady=5)
        
        # Просмотр состава бригады
        ttk.Button(team_manage_frame, text="Показать состав", 
                  command=self.show_team_members).grid(row=0, column=5, padx=5, pady=5)
        
        # Завершение заказов
        order_manage_frame = ttk.LabelFrame(self.manage_frame, text="Управление заказами")
        order_manage_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(order_manage_frame, text="Заказ:").grid(row=0, column=0, padx=5, pady=5)
        self.order_combo = ttk.Combobox(order_manage_frame, state="readonly")
        self.order_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(order_manage_frame, text="Завершить заказ", 
                  command=self.complete_order_gui).grid(row=0, column=2, padx=5, pady=5)
        
        # Фрейм для таблицы управления
        manage_table_frame = ttk.Frame(self.manage_frame)
        manage_table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Таблица для отображения результатов
        self.manage_tree = ttk.Treeview(manage_table_frame)
        self.manage_tree.pack(fill='both', expand=True, side='left')
        
        # Scrollbar для таблицы управления
        manage_scrollbar = ttk.Scrollbar(manage_table_frame, orient="vertical", command=self.manage_tree.yview)
        manage_scrollbar.pack(side='right', fill='y')
        self.manage_tree.configure(yscrollcommand=manage_scrollbar.set)
    
    def delete_selected(self):
        """Удаляет выбранную запись из текущего представления"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        
        item = selected_item[0]
        item_values = self.tree.item(item, 'values')
        if not item_values:
            return
        
        view_type = self.view_var.get()
        item_id = int(item_values[0])
        
        try:
            if view_type == "components":
                self.system.delete_component(item_id)
            elif view_type == "models":
                self.system.delete_model(item_id)
            elif view_type == "employees":
                self.system.delete_employee(item_id)
            elif view_type == "teams":
                self.system.delete_team(item_id)
            elif view_type == "orders":
                self.system.delete_order(item_id)
            elif view_type == "reports":
                self.system.delete_report(item_id)
            
            messagebox.showinfo("Успех", "Запись успешно удалена!")
            self.refresh_view()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")

    def show_add_form(self):
        # Очищаем предыдущую форму
        for widget in self.add_form_frame.winfo_children():
            widget.destroy()
        
        add_type = self.add_var.get()
        
        if add_type == "component":
            self.create_component_form()
        elif add_type == "model":
            self.create_model_form()
        elif add_type == "employee":
            self.create_employee_form()
        elif add_type == "team":
            self.create_team_form()
        elif add_type == "order":
            self.create_order_form()
        elif add_type == "report":
            self.create_report_form()
    
    def create_component_form(self):
        ttk.Label(self.add_form_frame, text="Наименование:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.comp_name = ttk.Entry(self.add_form_frame)
        self.comp_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Единица измерения:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.comp_unit = ttk.Entry(self.add_form_frame)
        self.comp_unit.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Срок годности:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.comp_expiry = ttk.Entry(self.add_form_frame)
        self.comp_expiry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Количество:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.comp_quantity = ttk.Entry(self.add_form_frame)
        self.comp_quantity.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить комплектующее", 
                  command=self.add_component_gui).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_model_form(self):
        ttk.Label(self.add_form_frame, text="Название модели:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.model_name = ttk.Entry(self.add_form_frame)
        self.model_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить модель", 
                  command=self.add_model_gui).grid(row=1, column=0, columnspan=2, pady=10)
    
    def create_employee_form(self):
        ttk.Label(self.add_form_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.emp_name = ttk.Entry(self.add_form_frame)
        self.emp_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Должность:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.emp_position = ttk.Entry(self.add_form_frame)
        self.emp_position.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить сотрудника", 
                  command=self.add_employee_gui).grid(row=2, column=0, columnspan=2, pady=10)
    
    def create_team_form(self):
        ttk.Label(self.add_form_frame, text="Название бригады:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.team_name = ttk.Entry(self.add_form_frame)
        self.team_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить бригаду", 
                  command=self.add_team_gui).grid(row=1, column=0, columnspan=2, pady=10)
    
    def create_order_form(self):
        ttk.Label(self.add_form_frame, text="Модель:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.order_model = ttk.Combobox(self.add_form_frame, state="readonly")
        self.order_model.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Количество:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.order_quantity = ttk.Entry(self.add_form_frame)
        self.order_quantity.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Бригада:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.order_team = ttk.Combobox(self.add_form_frame, state="readonly")
        self.order_team.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Срок (недель):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.order_weeks = ttk.Entry(self.add_form_frame)
        self.order_weeks.insert(0, "1")
        self.order_weeks.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить заказ", 
                  command=self.add_order_gui).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Обновляем комбобоксы для формы заказа
        self.refresh_order_comboboxes()
    
    def create_report_form(self):
        ttk.Label(self.add_form_frame, text="Заказ:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.report_order = ttk.Combobox(self.add_form_frame, state="readonly")
        self.report_order.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Собрано единиц:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.report_assembled = ttk.Entry(self.add_form_frame)
        self.report_assembled.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Количество брака:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.report_defects = ttk.Entry(self.add_form_frame)
        self.report_defects.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_form_frame, text="Затраченное время (часов):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.report_time = ttk.Entry(self.add_form_frame)
        self.report_time.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить отчет", 
                  command=self.add_report_gui).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Обновляем комбобоксы для формы отчета
        self.refresh_report_comboboxes()
    
    def refresh_data(self):
        self.refresh_view()
        # Обновляем комбобоксы только если они уже созданы
        if hasattr(self, 'team_combo') and self.team_combo:
            self.refresh_comboboxes()
    
    def refresh_view(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        view_type = self.view_var.get()
        
        if view_type == "components":
            self.show_components()
        elif view_type == "models":
            self.show_models()
        elif view_type == "employees":
            self.show_employees()
        elif view_type == "teams":
            self.show_teams()
        elif view_type == "orders":
            self.show_orders()
        elif view_type == "reports":
            self.show_reports()
    
    def refresh_comboboxes(self):
        """Обновляет все комбобоксы в интерфейсе"""
        # Обновляем комбобоксы в управлении
        models = self.system.get_models()
        teams = self.system.get_teams()
        employees = self.system.get_employees()
        orders = self.system.get_orders()
        
        if models and hasattr(self, 'order_model') and self.order_model:
            self.order_model['values'] = [f"{m['model_id']}. {m['model_name']}" for m in models]
        
        if teams and hasattr(self, 'team_combo') and self.team_combo:
            self.team_combo['values'] = [f"{t['team_id']}. {t['team_name']}" for t in teams]
        
        if employees and hasattr(self, 'employee_combo') and self.employee_combo:
            self.employee_combo['values'] = [f"{e['employee_id']}. {e['full_name']}" for e in employees]
        
        if orders and hasattr(self, 'order_combo') and self.order_combo:
            self.order_combo['values'] = [f"{o['order_id']}. {o['model_name']} ({o['quantity']} шт.)" for o in orders]
    
    def refresh_order_comboboxes(self):
        """Обновляет комбобоксы для формы заказа"""
        models = self.system.get_models()
        teams = self.system.get_teams()
        
        if models and hasattr(self, 'order_model') and self.order_model:
            self.order_model['values'] = [f"{m['model_id']}. {m['model_name']}" for m in models]
        
        if teams and hasattr(self, 'order_team') and self.order_team:
            # Показываем только свободные бригады
            busy_teams = self.system.get_busy_teams()
            busy_ids = [t['team_id'] for t in busy_teams]
            free_teams = [t for t in teams if t['team_id'] not in busy_ids]
            self.order_team['values'] = [f"{t['team_id']}. {t['team_name']} (Свободна)" for t in free_teams]
    
    def refresh_report_comboboxes(self):
        """Обновляет комбобоксы для формы отчета"""
        orders = self.system.get_orders()
        
        if orders and hasattr(self, 'report_order') and self.report_order:
            self.report_order['values'] = [f"{o['order_id']}. {o['model_name']} ({o['quantity']} шт.)" for o in orders]

    def show_components(self):
        self.tree['columns'] = ('ID', 'Наименование', 'Единица', 'Срок годности', 'Количество')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')  # Фиксированная ширина
        
        components = self.system.get_components()
        for comp in components:
            expiry = comp['expiry_date'].strftime('%d.%m.%Y') if comp['expiry_date'] else 'N/A'
            self.tree.insert('', 'end', values=(
                comp['component_id'],
                comp['component_name'],
                comp['unit'] or '',
                expiry,
                comp['quantity']
            ))

    def show_models(self):
        self.tree['columns'] = ('ID', 'Название модели')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300, anchor='center')  # Фиксированная ширина
        
        models = self.system.get_models()
        for model in models:
            self.tree.insert('', 'end', values=(
                model['model_id'],
                model['model_name']
            ))

    def show_employees(self):
        self.tree['columns'] = ('ID', 'ФИО', 'Должность')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor='center')  # Фиксированная ширина
        
        employees = self.system.get_employees()
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp['employee_id'],
                emp['full_name'],
                emp['position'] or ''
            ))

    def show_teams(self):
        self.tree['columns'] = ('ID', 'Название')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300, anchor='center')  # Фиксированная ширина
        
        teams = self.system.get_teams()
        for team in teams:
            self.tree.insert('', 'end', values=(
                team['team_id'],
                team['team_name']
            ))

    def show_orders(self):
        self.tree['columns'] = ('ID', 'Модель', 'Начало', 'Окончание', 'Кол-во', 'Бригада', 'Статус')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')  # Фиксированная ширина
        
        orders = self.system.get_orders()
        for order in orders:
            start_date = order['start_date'].strftime('%d.%m.%Y') if order['start_date'] else 'N/A'
            end_date = order['end_date'].strftime('%d.%m.%Y') if order['end_date'] else 'N/A'
            self.tree.insert('', 'end', values=(
                order['order_id'],
                order['model_name'],
                start_date,
                end_date,
                order['quantity'],
                order['team_name'],
                order['status']
            ))

    def show_reports(self):
        self.tree['columns'] = ('ID', 'Модель', 'Дата', 'Собрано', 'Брак', 'Время', 'Бригада', 'Заказано')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')  # Фиксированная ширина
        
        reports = self.system.get_order_reports()
        for report in reports:
            report_date = report['report_date'].strftime('%d.%m.%Y') if report['report_date'] else 'N/A'
            self.tree.insert('', 'end', values=(
                report['report_id'],
                report['model_name'],
                report_date,
                report['assembled_units'] or 0,
                report['defect_quantity'] or 0,
                report['time_spent'] or 0,
                report['team_name'],
                report['ordered_quantity'] or 0
            ))

    # Методы добавления данных (остаются без изменений из предыдущей версии)
    def add_component_gui(self):
        try:
            name = self.comp_name.get()
            unit = self.comp_unit.get()
            expiry = self.comp_expiry.get() or None
            quantity = int(self.comp_quantity.get())
            
            if not name:
                messagebox.showerror("Ошибка", "Введите наименование комплектующего")
                return
                
            result = self.system.add_component(name, unit, expiry, quantity)
            if result:
                messagebox.showinfo("Успех", "Комплектующее успешно добавлено!")
                self.comp_name.delete(0, 'end')
                self.comp_unit.delete(0, 'end')
                self.comp_expiry.delete(0, 'end')
                self.comp_quantity.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить комплектующее")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def add_model_gui(self):
        try:
            name = self.model_name.get()
            
            if not name:
                messagebox.showerror("Ошибка", "Введите название модели")
                return
                
            result = self.system.add_model(name)
            if result:
                messagebox.showinfo("Успех", "Модель успешно добавлена!")
                self.model_name.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить модель")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_employee_gui(self):
        try:
            name = self.emp_name.get()
            position = self.emp_position.get()
            
            if not name:
                messagebox.showerror("Ошибка", "Введите ФИО сотрудника")
                return
                
            result = self.system.add_employee(name, position)
            if result:
                messagebox.showinfo("Успех", "Сотрудник успешно добавлен!")
                self.emp_name.delete(0, 'end')
                self.emp_position.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить сотрудника")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_team_gui(self):
        try:
            name = self.team_name.get()
            
            if not name:
                messagebox.showerror("Ошибка", "Введите название бригады")
                return
                
            result = self.system.add_team(name)
            if result:
                messagebox.showinfo("Успех", "Бригада успешно добавлена!")
                self.team_name.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить бригаду")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_order_gui(self):
        try:
            model_str = self.order_model.get()
            quantity = int(self.order_quantity.get())
            team_str = self.order_team.get()
            weeks = int(self.order_weeks.get() or 1)
            
            if not model_str or not team_str:
                messagebox.showerror("Ошибка", "Выберите модель и бригаду")
                return
            
            model_id = int(model_str.split('.')[0])
            team_id = int(team_str.split('.')[0])
            
            result = self.system.add_order(model_id, quantity, team_id, weeks)
            if result:
                messagebox.showinfo("Успех", "Заказ успешно добавлен!")
                self.order_quantity.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить заказ")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def add_report_gui(self):
        try:
            order_str = self.report_order.get()
            assembled = int(self.report_assembled.get())
            defects = int(self.report_defects.get())
            time_spent = int(self.report_time.get())
            
            if not order_str:
                messagebox.showerror("Ошибка", "Выберите заказ")
                return
            
            if assembled < defects:
                messagebox.showerror("Ошибка", "Количество брака не может быть больше собранных единиц")
                return
            
            order_id = int(order_str.split('.')[0])
            
            result = self.system.add_order_report(order_id, assembled, defects, time_spent)
            if result:
                messagebox.showinfo("Успех", "Отчет успешно добавлен/обновлен!")
                self.report_assembled.delete(0, 'end')
                self.report_defects.delete(0, 'end')
                self.report_time.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить отчет")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    # Методы управления (остаются без изменений из предыдущей версии)
    def add_employee_to_team_gui(self):
        try:
            team_str = self.team_combo.get()
            employee_str = self.employee_combo.get()
            
            if not team_str or not employee_str:
                messagebox.showerror("Ошибка", "Выберите бригаду и сотрудника")
                return
            
            team_id = int(team_str.split('.')[0])
            employee_id = int(employee_str.split('.')[0])
            
            result = self.system.add_employee_to_team(team_id, employee_id)
            if result:
                messagebox.showinfo("Успех", "Сотрудник успешно добавлен в бригаду!")
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить сотрудника в бригаду")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def show_team_members(self):
        try:
            team_str = self.team_combo.get()
            if not team_str:
                messagebox.showerror("Ошибка", "Выберите бригаду")
                return
            
            team_id = int(team_str.split('.')[0])
            members = self.system.get_team_members(team_id)
            
            # Очищаем таблицу
            for item in self.manage_tree.get_children():
                self.manage_tree.delete(item)
            
            self.manage_tree['columns'] = ('ID', 'ФИО', 'Должность')
            for col in self.manage_tree['columns']:
                self.manage_tree.heading(col, text=col)
                self.manage_tree.column(col, width=150, anchor='center')  # Фиксированная ширина
            
            if members:
                for member in members:
                    self.manage_tree.insert('', 'end', values=(
                        member['employee_id'],
                        member['full_name'],
                        member['position'] or ''
                    ))
            else:
                messagebox.showinfo("Информация", "В этой бригаде нет сотрудников")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def complete_order_gui(self):
        try:
            order_str = self.order_combo.get()
            if not order_str:
                messagebox.showerror("Ошибка", "Выберите заказ")
                return
            
            order_id = int(order_str.split('.')[0])
            result = self.system.complete_order(order_id)
            if result:
                messagebox.showinfo("Успех", "Заказ успешно завершен!")
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось завершить заказ")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")
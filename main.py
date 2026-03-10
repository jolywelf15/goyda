import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
from models import SmartphoneAssemblySystem


class LoginWindow:
    def __init__(self, db_system):
        self.db_system = db_system
        self.current_user = None
        
        self.root = tk.Tk()
        self.root.title("Авторизация - Система сборки смартфонов")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Центрирование окна
        self.center_window(400, 300)
        
        # Запрещаем закрытие через крестик
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
    
    def center_window(self, width, height):
        """Центрирование окна на экране"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Система сборки смартфонов", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Подзаголовок
        subtitle_label = tk.Label(
            self.root, 
            text="Войдите в систему", 
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Фрейм для формы
        form_frame = ttk.Frame(self.root)
        form_frame.pack(padx=40, pady=10, fill='x')
        
        # Поле логина
        ttk.Label(form_frame, text="Логин:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Поле пароля
        ttk.Label(form_frame, text="Пароль:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="•")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Кнопки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="Войти", 
            command=self.login,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="Выход", 
            command=self.exit_app,
            width=15
        ).pack(side='left', padx=5)
        
        # Информация о стандартном пользователе
        info_label = tk.Label(
            self.root, 
            text="Пользователь: admin / admin123",
            font=("Arial", 8),
            fg="#95a5a6"
        )
        info_label.pack(pady=(10, 0))
        
        # Связываем Enter с кнопкой входа
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Фокус на поле логина
        self.username_entry.focus_set()
    
    def login(self):
        """Обработка входа в систему"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        try:
            user = self.db_system.authenticate(username, password)
            
            if user:
                self.current_user = user
                messagebox.showinfo(
                    "Успешный вход", 
                    f"Добро пожаловать, {user['full_name']}!"
                )
                self.root.destroy()  # Закрываем окно авторизации
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
                self.password_entry.delete(0, 'end')
                self.password_entry.focus_set()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка авторизации: {str(e)}")
    
    def exit_app(self):
        """Выход из приложения"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.quit()
    
    def on_closing(self):
        """Обработка закрытия окна"""
        self.exit_app()
    
    def get_current_user(self):
        """Возвращает текущего авторизованного пользователя"""
        return self.current_user
    
    def run(self):
        """Запускает окно авторизации"""
        self.root.mainloop()
        return self.current_user


class SmartphoneAssemblyApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        
        self.root.title(f"Система сборки смартфонов - {current_user['full_name']}")
        self.root.geometry("1200x700")
        
        self.system = SmartphoneAssemblySystem()
        
        # Инициализируем переменные для комбобоксов
        self.order_model = None
        self.order_team = None
        self.team_combo = None
        self.employee_combo = None
        self.order_combo = None
        self.report_order = None
        
        # Создаем меню
        self.create_menu()
        
        self.create_widgets()
        self.refresh_data()
    
    def create_menu(self):
        """Создает верхнее меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Система", menu=file_menu)
        file_menu.add_command(label="Выйти из системы", command=self.logout)
    
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из системы?"):
            self.root.destroy()
    
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
            ("Склад комплектующих", "components"),
            ("Модели смартфонов", "models"),
            ("Сотрудники", "employees"),
            ("Бригады", "teams"),
            ("Заказы", "orders"),
            ("Отчеты", "reports")
        ]
        
        for text, value in view_types:
            ttk.Radiobutton(view_selector_frame, text=text, variable=self.view_var, 
                           value=value, command=self.refresh_view).pack(side='left', padx=5)
        
        # Фрейм для таблицы и кнопок
        table_frame = ttk.Frame(self.view_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Создаем фрейм для таблицы с scrollbar
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Таблица для отображения данных
        self.tree = ttk.Treeview(tree_frame)
        
        # Scrollbar для таблицы
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Размещаем таблицу и скроллбары
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Настраиваем веса для растягивания
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(self.view_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        # Кнопка удаления выбранной записи
        delete_button = ttk.Button(button_frame, text="Удалить выбранное", 
                                 command=self.delete_selected)
        delete_button.pack(side='left', padx=5)
        
        # Кнопка экспорта в Excel
        export_button = ttk.Button(button_frame, text="Экспорт в Excel", 
                                 command=self.export_to_excel)
        export_button.pack(side='left', padx=5)
        
        # Кнопка обновления данных
    
    
    def create_add_tab(self):
        # Фрейм для выбора типа добавляемых данных
        add_selector_frame = ttk.Frame(self.add_frame)
        add_selector_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_selector_frame, text="Добавить:").pack(side='left')
        
        self.add_var = tk.StringVar(value="component")
        add_types = [
            ("Комплектующее", "component"),
            ("Модель смартфона", "model"),
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
        
        # Создаем фрейм для таблицы управления с scrollbar
        manage_tree_frame = ttk.Frame(manage_table_frame)
        manage_tree_frame.pack(fill='both', expand=True)
        
        # Таблица для отображения результатов
        self.manage_tree = ttk.Treeview(manage_tree_frame)
        
        # Scrollbar для таблицы управления
        manage_v_scrollbar = ttk.Scrollbar(manage_tree_frame, orient="vertical", command=self.manage_tree.yview)
        manage_h_scrollbar = ttk.Scrollbar(manage_tree_frame, orient="horizontal", command=self.manage_tree.xview)
        
        self.manage_tree.configure(yscrollcommand=manage_v_scrollbar.set, xscrollcommand=manage_h_scrollbar.set)
        
        # Размещаем таблицу и скроллбары
        self.manage_tree.grid(row=0, column=0, sticky='nsew')
        manage_v_scrollbar.grid(row=0, column=1, sticky='ns')
        manage_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Настраиваем веса для растягивания
        manage_tree_frame.grid_rowconfigure(0, weight=1)
        manage_tree_frame.grid_columnconfigure(0, weight=1)
    
    def export_to_excel(self):
        """Экспортирует текущие данные в Excel файл"""
        try:
            view_type = self.view_var.get()
            
            # Получаем данные в зависимости от типа просмотра
            if view_type == "components":
                data = self.system.get_components()
                filename = "склад_комплектующих"
            elif view_type == "models":
                data = self.system.get_models()
                filename = "модели_смартфонов"
            elif view_type == "employees":
                data = self.system.get_employees()
                filename = "сотрудники"
            elif view_type == "teams":
                data = self.system.get_teams()
                filename = "бригады"
            elif view_type == "orders":
                data = self.system.get_orders()
                filename = "заказы"
            elif view_type == "reports":
                data = self.system.get_order_reports()
                filename = "отчеты"
            else:
                messagebox.showerror("Ошибка", "Неизвестный тип данных для экспорта")
                return
            
            if not data:
                messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
                return
            
            # Преобразуем данные в DataFrame
            df = pd.DataFrame(data)
            
            # Запрашиваем место сохранения файла
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"{filename}_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.xlsx"
            )
            
            if file_path:
                # Сохраняем в Excel
                df.to_excel(file_path, index=False, engine='openpyxl')
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в файл:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте в Excel: {str(e)}")
    
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
            result = False
            if view_type == "components":
                result = self.system.delete_component(item_id)
            elif view_type == "models":
                result = self.system.delete_model(item_id)
            elif view_type == "employees":
                result = self.system.delete_employee(item_id)
            elif view_type == "teams":
                result = self.system.delete_team(item_id)
            elif view_type == "orders":
                result = self.system.delete_order(item_id)
            elif view_type == "reports":
                result = self.system.delete_report(item_id)
            
            if result:
                messagebox.showinfo("Успех", "Запись успешно удалена!")
                self.refresh_view()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить запись")
            
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
        
        ttk.Label(self.add_form_frame, text="Количество:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.comp_quantity = ttk.Entry(self.add_form_frame)
        self.comp_quantity.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить комплектующее", 
                  command=self.add_component_gui).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_model_form(self):
        ttk.Label(self.add_form_frame, text="Название модели:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.model_name = ttk.Entry(self.add_form_frame)
        self.model_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить модель смартфона", 
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
        ttk.Label(self.add_form_frame, text="Модель смартфона:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
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
        
        # Добавляем информационную метку о дате
        ttk.Label(self.add_form_frame, text="Дата окончания сборки будет установлена автоматически", 
                  foreground="gray").grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.add_form_frame, text="Добавить отчет", 
                  command=self.add_report_gui).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Обновляем комбобоксы для формы отчета
        self.refresh_report_comboboxes()
    
    def refresh_data(self):
        self.refresh_view()
        # Обновляем комбобоксы только если они уже созданы
        if hasattr(self, 'team_combo') and self.team_combo and self.team_combo.winfo_exists():
            self.refresh_comboboxes()
    
    def refresh_view(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Очищаем колонки
        self.tree['columns'] = ()
        
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
        try:
            # Обновляем комбобоксы в управлении
            models = self.system.get_models()
            teams = self.system.get_teams()
            employees = self.system.get_employees()
            orders = self.system.get_orders()
            
            # Проверяем существование комбобоксов перед обновлением
            if (models and hasattr(self, 'order_model') and self.order_model and 
                self.order_model.winfo_exists()):
                self.order_model['values'] = [f"{m['model_id']}. {m['model_name']}" for m in models]
            
            if (teams and hasattr(self, 'team_combo') and self.team_combo and 
                self.team_combo.winfo_exists()):
                self.team_combo['values'] = [f"{t['team_id']}. {t['team_name']}" for t in teams]
            
            if (employees and hasattr(self, 'employee_combo') and self.employee_combo and 
                self.employee_combo.winfo_exists()):
                self.employee_combo['values'] = [f"{e['employee_id']}. {e['full_name']}" for e in employees]
            
            if (orders and hasattr(self, 'order_combo') and self.order_combo and 
                self.order_combo.winfo_exists()):
                self.order_combo['values'] = [f"{o['order_id']}. {o['model_name']} ({o['quantity']} шт.)" for o in orders]
                
        except Exception as e:
            print(f"Ошибка при обновлении комбобоксов: {e}")
    
    def refresh_order_comboboxes(self):
        """Обновляет комбобоксы для формы заказа"""
        try:
            models = self.system.get_models()
            teams = self.system.get_teams()
            
            if (models and hasattr(self, 'order_model') and self.order_model and 
                self.order_model.winfo_exists()):
                self.order_model['values'] = [f"{m['model_id']}. {m['model_name']}" for m in models]
            
            if (teams and hasattr(self, 'order_team') and self.order_team and 
                self.order_team.winfo_exists()):
                # Показываем только свободные бригады
                busy_teams = self.system.get_busy_teams()
                busy_ids = [t['team_id'] for t in busy_teams]
                free_teams = [t for t in teams if t['team_id'] not in busy_ids]
                self.order_team['values'] = [f"{t['team_id']}. {t['team_name']} (Свободна)" for t in free_teams]
        except Exception as e:
            print(f"Ошибка при обновлении комбобоксов заказа: {e}")
    
    def refresh_report_comboboxes(self):
        """Обновляет комбобоксы для формы отчета"""
        try:
            orders = self.system.get_orders()
            
            if (orders and hasattr(self, 'report_order') and self.report_order and 
                self.report_order.winfo_exists()):
                self.report_order['values'] = [f"{o['order_id']}. {o['model_name']} ({o['quantity']} шт.)" for o in orders]
        except Exception as e:
            print(f"Ошибка при обновлении комбобоксов отчета: {e}")

    def show_components(self):
        self.tree['columns'] = ('ID', 'Наименование', 'Единица', 'Количество')
        
        # Настраиваем столбцы с фиксированными размерами
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Наименование', width=250, minwidth=250, stretch=tk.NO)
        self.tree.column('Единица', width=120, minwidth=120, stretch=tk.NO)
        self.tree.column('Количество', width=100, minwidth=100, stretch=tk.NO)
        
        # Устанавливаем заголовки
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        components = self.system.get_components()
        for comp in components:
            self.tree.insert('', 'end', values=(
                comp['component_id'],
                comp['component_name'],
                comp['unit'] or '',
                comp['quantity']
            ))

    def show_models(self):
        self.tree['columns'] = ('ID', 'Название модели')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Название модели', width=300, minwidth=300, stretch=tk.NO)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        models = self.system.get_models()
        for model in models:
            self.tree.insert('', 'end', values=(
                model['model_id'],
                model['model_name']
            ))

    def show_employees(self):
        self.tree['columns'] = ('ID', 'ФИО', 'Должность')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('ФИО', width=250, minwidth=250, stretch=tk.NO)
        self.tree.column('Должность', width=200, minwidth=200, stretch=tk.NO)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        employees = self.system.get_employees()
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp['employee_id'],
                emp['full_name'],
                emp['position'] or ''
            ))

    def show_teams(self):
        self.tree['columns'] = ('ID', 'Название')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Название', width=300, minwidth=300, stretch=tk.NO)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        teams = self.system.get_teams()
        for team in teams:
            self.tree.insert('', 'end', values=(
                team['team_id'],
                team['team_name']
            ))

    def format_date(self, date_str):
        """Форматирует дату из строки в формат дд-мм-гггг"""
        if not date_str:
            return 'N/A'
        
        if isinstance(date_str, str):
            # Если дата в формате ГГГГ-ММ-ДД
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                return f"{date_str[8:10]}-{date_str[5:7]}-{date_str[0:4]}"
            # Если дата уже в формате дд-мм-гггг
            elif len(date_str) == 10 and date_str[2] == '-' and date_str[5] == '-':
                return date_str
            # Если это другой формат, пытаемся преобразовать
            else:
                try:
                    # Пробуем разные форматы
                    for fmt in ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y']:
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            return date_obj.strftime('%d-%m-%Y')
                        except:
                            continue
                except:
                    pass
        
        return 'N/A'

    def show_orders(self):
        self.tree['columns'] = ('ID', 'Модель', 'Начало', 'Окончание', 'Кол-во', 'Бригада', 'Статус')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Модель', width=150, minwidth=150, stretch=tk.NO)
        self.tree.column('Начало', width=100, minwidth=100, stretch=tk.NO)
        self.tree.column('Окончание', width=100, minwidth=100, stretch=tk.NO)
        self.tree.column('Кол-во', width=80, minwidth=80, stretch=tk.NO)
        self.tree.column('Бригада', width=150, minwidth=150, stretch=tk.NO)
        self.tree.column('Статус', width=100, minwidth=100, stretch=tk.NO)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        orders = self.system.get_orders()
        for order in orders:
            # Форматируем даты в формат дд-мм-гггг
            start_date = self.format_date(order['start_date'])
            end_date = self.format_date(order['end_date'])
                
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
        self.tree['columns'] = ('ID', 'Модель', 'Дата окончания', 'Собрано', 'Брак', 'Время', 'Бригада', 'Заказано')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Модель', width=150, minwidth=150, stretch=tk.NO)
        self.tree.column('Дата окончания', width=120, minwidth=120, stretch=tk.NO)
        self.tree.column('Собрано', width=80, minwidth=80, stretch=tk.NO)
        self.tree.column('Брак', width=80, minwidth=80, stretch=tk.NO)
        self.tree.column('Время', width=80, minwidth=80, stretch=tk.NO)
        self.tree.column('Бригада', width=150, minwidth=150, stretch=tk.NO)
        self.tree.column('Заказано', width=80, minwidth=80, stretch=tk.NO)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        reports = self.system.get_order_reports()
        for report in reports:
            # Форматируем дату отчета в формат дд-мм-гггг
            report_date = self.format_date(report['report_date'])
                
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

    # Методы добавления данных
    def add_component_gui(self):
        try:
            name = self.comp_name.get()
            unit = self.comp_unit.get()
            quantity = int(self.comp_quantity.get())
            
            if not name:
                messagebox.showerror("Ошибка", "Введите наименование комплектующего")
                return
                
            result = self.system.add_component(name, unit, None, quantity)
            if result:
                messagebox.showinfo("Успех", "Комплектующее успешно добавлено!")
                self.comp_name.delete(0, 'end')
                self.comp_unit.delete(0, 'end')
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
                messagebox.showinfo("Успех", "Модель смартфона успешно добавлена!")
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
                current_date = datetime.now().strftime('%d-%m-%Y')
                messagebox.showinfo("Успех", f"Отчет успешно добавлен!\nДата окончания сборки: {current_date}")
                self.report_assembled.delete(0, 'end')
                self.report_defects.delete(0, 'end')
                self.report_time.delete(0, 'end')
                self.refresh_data()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить отчет")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    # Методы управления
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
            
            # Очищаем колонки
            self.manage_tree['columns'] = ()
            
            self.manage_tree['columns'] = ('ID', 'ФИО', 'Должность')
            
            # Настраиваем столбцы с фиксированными размерами
            self.manage_tree.column('#0', width=0, stretch=tk.NO)
            self.manage_tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
            self.manage_tree.column('ФИО', width=250, minwidth=250, stretch=tk.NO)
            self.manage_tree.column('Должность', width=200, minwidth=200, stretch=tk.NO)
            
            for col in self.manage_tree['columns']:
                self.manage_tree.heading(col, text=col)
            
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

# ========== ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ==========

def start_application():
    """Запускает приложение с авторизацией"""
    
    print("=" * 50)
    print("🔄 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ СБОРКИ СМАРТФОНОВ")
    print("=" * 50)
    
    try:
        # Инициализируем систему базы данных
        print("📊 Подключение к базе данных...")
        system = SmartphoneAssemblySystem()
        
        # Окно авторизации
        print("🔐 Запуск авторизации...")
        login_window = LoginWindow(system)
        user = login_window.run()
        
        # Если авторизация успешна - запускаем основное приложение
        if user:
            print(f"✅ Привет, {user['full_name']}!")
            print("🚀 Запуск основного приложения...")
            
            # Запускаем основное приложение
            root = tk.Tk()
            app = SmartphoneAssemblyApp(root, user)
            
            # Центрируем окно
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - 1200) // 2
            y = (screen_height - 700) // 2
            root.geometry(f"1200x700+{x}+{y}")
            
            root.mainloop()
        else:
            print("❌ Авторизация отменена")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        print("Проверьте:")
        print("1. Запущен ли MySQL в XAMPP")
        print("2. Правильный ли пароль в настройках")
        print("3. Существует ли база данных 'smartphone_assembly'")
        input("Нажмите Enter для выхода...")

def main():
    """Точка входа в приложение"""
    start_application()

if __name__ == "__main__":
    main()
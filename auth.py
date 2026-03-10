import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class LoginWindow:
    def __init__(self, db_system):
        self.db_system = db_system
        self.current_user = None
        
        self.root = tk.Tk()
        self.root.title("Авторизация - Система сборки смартфонов")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Устанавливаем иконку (если есть)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Центрирование окна
        self.center_window(500, 400)
        
        # Запрещаем закрытие через крестик
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Создаем стили для виджетов
        self.setup_styles()
        
        self.create_widgets()
        
        # Фокус на поле логина
        self.root.after(100, lambda: self.username_entry.focus_set())
    
    def setup_styles(self):
        """Настраивает стили для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стиль для кнопок
        style.configure('Login.TButton', 
                       font=('Arial', 11, 'bold'),
                       padding=10,
                       background='#4CAF50',
                       foreground='white')
        
        style.configure('Exit.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=10,
                       background='#f44336',
                       foreground='white')
        
        style.map('Login.TButton',
                 background=[('active', '#45a049')])
        
        style.map('Exit.TButton',
                 background=[('active', '#d32f2f')])
        
        # Стиль для полей ввода
        style.configure('Login.TEntry',
                       font=('Arial', 11),
                       padding=8)
    
    def center_window(self, width, height):
        """Центрирование окна на экране"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Система сборки смартфонов", 
            font=("Arial", 20, "bold"),
            fg="#2c3e50",
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 10))
        
        # Подзаголовок
        subtitle_label = tk.Label(
            main_frame, 
            text="Войдите в систему для доступа к функциям", 
            font=("Arial", 11),
            fg="#7f8c8d",
            bg='#f0f0f0'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Фрейм для формы входа
        form_frame = ttk.LabelFrame(main_frame, text="Данные для входа", padding="20")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Поле логина
        login_frame = ttk.Frame(form_frame)
        login_frame.pack(fill='x', pady=10)
        
        ttk.Label(
            login_frame, 
            text="Логин:", 
            font=("Arial", 11, "bold"),
            width=15
        ).pack(side='left', padx=(0, 10))
        
        self.username_entry = ttk.Entry(
            login_frame, 
            font=("Arial", 11),
            width=25
        )
        self.username_entry.pack(side='left')
        
        # Поле пароля
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill='x', pady=10)
        
        ttk.Label(
            password_frame, 
            text="Пароль:", 
            font=("Arial", 11, "bold"),
            width=15
        ).pack(side='left', padx=(0, 10))
        
        self.password_entry = ttk.Entry(
            password_frame, 
            font=("Arial", 11),
            width=25,
            show="•"
        )
        self.password_entry.pack(side='left')
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Кнопка входа
        login_button = ttk.Button(
            button_frame, 
            text="Войти в систему", 
            command=self.login,
            style='Login.TButton',
            width=20
        )
        login_button.pack(side='left', padx=10)
        
        # Кнопка выхода
        exit_button = ttk.Button(
            button_frame, 
            text="Выход", 
            command=self.exit_app,
            style='Exit.TButton',
            width=20
        )
        exit_button.pack(side='left', padx=10)
        
        # Фрейм с информацией
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=10)
        
        # Информация о тестовом пользователе
        test_user_frame = ttk.LabelFrame(info_frame, text="Тестовый доступ", padding="10")
        test_user_frame.pack(fill='x', padx=10, pady=5)
        
        test_info = tk.Label(
            test_user_frame,
            text="Логин: admin\nПароль: 1234",
            font=("Arial", 10),
            fg="#2c3e50",
            bg='#f9f9f9',
            justify='left'
        )
        test_info.pack()
        
        # Информация о текущем времени
        time_frame = ttk.Frame(info_frame)
        time_frame.pack(fill='x', padx=10, pady=5)
        
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        time_label = tk.Label(
            time_frame,
            text=f"Дата и время: {current_time}",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg='#f0f0f0'
        )
        time_label.pack()
        
        # Связываем Enter с кнопкой входа
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Обработка Escape для выхода
        self.root.bind('<Escape>', lambda e: self.exit_app())
    
    def login(self):
        """Обработка входа в систему"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Проверка на пустые поля
        if not username or not password:
            messagebox.showerror(
                "Ошибка ввода", 
                "Пожалуйста, заполните все поля!\n\n" +
                "Введите логин и пароль для доступа к системе."
            )
            if not username:
                self.username_entry.focus_set()
            else:
                self.password_entry.focus_set()
            return
        
        # Показать индикатор загрузки
        self.show_loading(True)
        
        try:
            # Имитация задержки для реалистичности
            self.root.after(500, lambda: self.perform_login(username, password))
            
        except Exception as e:
            self.show_loading(False)
            messagebox.showerror(
                "Ошибка системы", 
                f"Произошла ошибка при подключении к базе данных:\n{str(e)}"
            )
    
    def perform_login(self, username, password):
        """Выполняет аутентификацию"""
        try:
            user = self.db_system.authenticate(username, password)
            
            if user:
                self.current_user = user
                self.show_loading(False)
                
                # Показать приветственное сообщение
                welcome_text = f"Добро пожаловать, {user['full_name']}!\n\n"
                welcome_text += f"Роль: {user['role'].capitalize()}\n"
                welcome_text += f"Время входа: {datetime.now().strftime('%H:%M:%S')}"
                
                messagebox.showinfo(
                    "Успешный вход", 
                    welcome_text,
                    icon='info'
                )
                
                # Закрываем окно авторизации
                self.root.destroy()
            else:
                self.show_loading(False)
                messagebox.showerror(
                    "Ошибка авторизации", 
                    "Неверный логин или пароль.\n\n" +
                    "Проверьте правильность введенных данных и попробуйте снова."
                )
                self.password_entry.delete(0, 'end')
                self.password_entry.focus_set()
                
        except Exception as e:
            self.show_loading(False)
            messagebox.showerror(
                "Ошибка подключения", 
                f"Не удалось подключиться к базе данных:\n{str(e)}\n\n" +
                "Проверьте:\n" +
                "1. Запущен ли MySQL сервер\n" +
                "2. Правильность настроек подключения"
            )
    
    def show_loading(self, show=True):
        """Показывает/скрывает индикатор загрузки"""
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
        
        if show:
            self.loading_label = tk.Label(
                self.root,
                text="Подключение к системе...",
                font=("Arial", 10, "italic"),
                fg="#3498db",
                bg='#f0f0f0'
            )
            self.loading_label.place(relx=0.5, rely=0.9, anchor='center')
            self.root.update()
    
    def exit_app(self):
        """Выход из приложения"""
        if messagebox.askyesno(
            "Подтверждение выхода", 
            "Вы уверены, что хотите выйти из системы?\n\n" +
            "Все несохраненные данные будут потеряны.",
            icon='warning'
        ):
            self.root.quit()
    
    def on_closing(self):
        """Обработка закрытия окна через крестик"""
        self.exit_app()
    
    def get_current_user(self):
        """Возвращает текущего авторизованного пользователя"""
        return self.current_user
    
    def run(self):
        """Запускает окно авторизации"""
        self.root.mainloop()
        return self.current_user


# Дополнительный класс для окна смены пароля (если понадобится в будущем)
class ChangePasswordWindow:
    def __init__(self, parent, db_system, user_id):
        self.parent = parent
        self.db_system = db_system
        self.user_id = user_id
        
        self.window = tk.Toplevel(parent)
        self.window.title("Смена пароля")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Делаем окно модальным
        self.window.transient(parent)
        self.window.grab_set()
        
        # Центрирование окна относительно родительского
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """Центрирует окно относительно родительского"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Смена пароля", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50",
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 20))
        
        # Фрейм для формы
        form_frame = ttk.LabelFrame(main_frame, text="Введите новый пароль", padding="15")
        form_frame.pack(fill='x', pady=10)
        
        # Старый пароль
        old_frame = ttk.Frame(form_frame)
        old_frame.pack(fill='x', pady=5)
        
        ttk.Label(old_frame, text="Старый пароль:", width=15).pack(side='left')
        self.old_password = ttk.Entry(old_frame, width=25, show="•")
        self.old_password.pack(side='left', padx=(10, 0))
        
        # Новый пароль
        new_frame = ttk.Frame(form_frame)
        new_frame.pack(fill='x', pady=5)
        
        ttk.Label(new_frame, text="Новый пароль:", width=15).pack(side='left')
        self.new_password = ttk.Entry(new_frame, width=25, show="•")
        self.new_password.pack(side='left', padx=(10, 0))
        
        # Подтверждение пароля
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill='x', pady=5)
        
        ttk.Label(confirm_frame, text="Подтверждение:", width=15).pack(side='left')
        self.confirm_password = ttk.Entry(confirm_frame, width=25, show="•")
        self.confirm_password.pack(side='left', padx=(10, 0))
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="Сохранить", 
            command=self.change_password,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="Отмена", 
            command=self.window.destroy,
            width=15
        ).pack(side='left', padx=5)
    
    def change_password(self):
        """Обработка смены пароля"""
        old_pass = self.old_password.get()
        new_pass = self.new_password.get()
        confirm_pass = self.confirm_password.get()
        
        if not all([old_pass, new_pass, confirm_pass]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if new_pass != confirm_pass:
            messagebox.showerror("Ошибка", "Новый пароль и подтверждение не совпадают")
            return
        
        if len(new_pass) < 4:
            messagebox.showerror("Ошибка", "Пароль должен быть не менее 4 символов")
            return
        
        # Здесь должна быть проверка старого пароля
        # и вызов метода смены пароля из db_system
        
        messagebox.showinfo("Успешно", "Пароль успешно изменен")
        self.window.destroy()
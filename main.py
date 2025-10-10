from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import socket
import threading
import time

class ChatApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        
        # Статус подключения
        self.status_label = Label(
            text='Не подключено',
            size_hint=(1, 0.05),
            color=(1, 0, 0, 1)  # Красный цвет
        )
        
        # Область сообщений
        self.chat_scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=None,
            spacing=5
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Панель подключения
        connect_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        
        self.server_ip_input = TextInput(
            hint_text='IP сервера',
            text='192.168.1.100',  # Замените на ваш IP
            size_hint=(0.4, 1),
            multiline=False
        )
        
        self.port_input = TextInput(
            hint_text='Порт',
            text='12345',
            size_hint=(0.2, 1),
            multiline=False
        )
        
        self.nickname_input = TextInput(
            hint_text='Имя',
            text='User',
            size_hint=(0.2, 1),
            multiline=False
        )
        
        self.connect_btn = Button(
            text='Подключиться',
            size_hint=(0.2, 1),
            background_color=(0, 1, 0, 1)
        )
        self.connect_btn.bind(on_press=self.toggle_connection)
        
        # Панель сообщения
        message_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        
        self.message_input = TextInput(
            hint_text='Введите сообщение...',
            size_hint=(0.7, 1),
            multiline=False
        )
        self.message_input.bind(on_text_validate=self.send_message)
        
        self.send_btn = Button(
            text='Отправить',
            size_hint=(0.3, 1),
            background_color=(0.2, 0.6, 1, 1)
        )
        self.send_btn.bind(on_press=self.send_message)
        
        # Сборка интерфейса
        connect_layout.add_widget(self.server_ip_input)
        connect_layout.add_widget(self.port_input)
        connect_layout.add_widget(self.nickname_input)
        connect_layout.add_widget(self.connect_btn)
        
        message_layout.add_widget(self.message_input)
        message_layout.add_widget(self.send_btn)
        
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.chat_scroll)
        main_layout.add_widget(connect_layout)
        main_layout.add_widget(message_layout)
        
        # Инициализация
        self.client_socket = None
        self.connected = False
        self.receive_thread = None
        self.nickname = "User"
        
        self.add_message("Система", "Приложение запущено. Введите данные для подключения")
        
        return main_layout
    
    def toggle_connection(self, instance):
        if self.connected:
            self.disconnect()
        else:
            self.connect_to_server()
    
    def connect_to_server(self):
        try:
            server_ip = self.server_ip_input.text.strip()
            port = int(self.port_input.text.strip())
            self.nickname = self.nickname_input.text.strip() or "User"
            
            self.update_status("Подключаемся...", (1, 1, 0, 1))  # Желтый
            self.add_message("Система", f"Попытка подключения к {server_ip}:{port}...")
            
            # Создаем сокет
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(10)  # Таймаут подключения 10 сек
            
            # Подключаемся
            self.client_socket.connect((server_ip, port))
            
            # Настраиваем таймаут для операций
            self.client_socket.settimeout(1.0)  # 1 секунда для recv
            
            self.connected = True
            self.connect_btn.text = "Отключиться"
            self.connect_btn.background_color = (1, 0, 0, 1)  # Красный
            self.update_status("Подключено", (0, 1, 0, 1))  # Зеленый
            
            self.add_message("Система", "✅ Успешное подключение!")
            
            # Отправляем никнейм
            try:
                self.client_socket.send(f"NICK:{self.nickname}".encode('utf-8'))
            except:
                pass
            
            # Запускаем поток приема сообщений
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            
        except socket.timeout:
            self.add_message("Ошибка", "❌ Таймаут подключения")
            self.update_status("Ошибка", (1, 0, 0, 1))
            self.cleanup_socket()
        except ConnectionRefusedError:
            self.add_message("Ошибка", "❌ Сервер недоступен")
            self.update_status("Ошибка", (1, 0, 0, 1))
            self.cleanup_socket()
        except Exception as e:
            self.add_message("Ошибка", f"❌ Ошибка: {str(e)}")
            self.update_status("Ошибка", (1, 0, 0, 1))
            self.cleanup_socket()
    
    def disconnect(self):
        self.connected = False
        self.cleanup_socket()
        self.connect_btn.text = "Подключиться"
        self.connect_btn.background_color = (0, 1, 0, 1)  # Зеленый
        self.update_status("Отключено", (1, 0, 0, 1))
        self.add_message("Система", "Отключено от сервера")
    
    def cleanup_socket(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
    
    def receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    if message.strip():
                        Clock.schedule_once(lambda dt, msg=message: self.add_message("Чат", msg))
                        
            except socket.timeout:
                continue  # Таймаут - нормально, продолжаем цикл
            except Exception as e:
                if self.connected:  # Только если еще подключены
                    print(f"Receive error: {e}")
                break
        
        if self.connected:  # Если разрыв не по нашей инициативе
            Clock.schedule_once(lambda dt: self.connection_lost())
    
    def connection_lost(self):
        self.add_message("Система", "❌ Соединение разорвано")
        self.disconnect()
    
    def send_message(self, instance):
        if not self.connected:
            self.add_message("Ошибка", "❌ Нет подключения")
            return
            
        message = self.message_input.text.strip()
        if not message:
            return
            
        try:
            # Добавляем перевод строки для сервера
            full_message = f"{message}\n"
            self.client_socket.send(full_message.encode('utf-8'))
            self.add_message("Вы", message)
            self.message_input.text = ''
        except Exception as e:
            self.add_message("Ошибка", f"❌ Ошибка отправки: {str(e)}")
            self.connection_lost()
    
    def update_status(self, text, color):
        self.status_label.text = f"Статус: {text}"
        self.status_label.color = color
    
    def add_message(self, sender, message):
        message_text = f"{sender}: {message}"
        message_label = Label(
            text=message_text,
            size_hint_y=None,
            height=40,
            text_size=(Window.width - 20, None),
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        message_label.bind(texture_size=message_label.setter('size'))
        
        # Цвет фона для сообщений
        with message_label.canvas.before:
            from kivy.graphics import Color, Rectangle
            if sender == "Вы":
                Color(0.1, 0.5, 0.8, 0.8)  # Синий
            elif sender == "Система":
                Color(0.8, 0.5, 0.1, 0.8)  # Оранжевый
            elif sender == "Ошибка":
                Color(0.8, 0.1, 0.1, 0.8)  # Красный
            else:
                Color(0.2, 0.2, 0.2, 0.8)  # Серый
            Rectangle(pos=message_label.pos, size=message_label.size)
        
        self.chat_layout.add_widget(message_label)
        Clock.schedule_once(lambda dt: self.chat_scroll.scroll_to(message_label))
    
    def on_stop(self):
        self.connected = False
        self.cleanup_socket()

if __name__ == '__main__':
    ChatApp().run()
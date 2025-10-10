import socket
import threading
import time

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = {}
        self.running = True
        
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(1)  # Таймаут для accept
            
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"✅ Сервер запущен на {self.host}:{self.port}")
            print("Ожидание подключений...")
            
            # Поток для очистки мертвых подключений
            cleaner_thread = threading.Thread(target=self.cleanup_clients, daemon=True)
            cleaner_thread.start()
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"✅ Новое подключение: {address}")
                    
                    # Настраиваем таймаут
                    client_socket.settimeout(1.0)
                    
                    # Добавляем клиента
                    client_info = {
                        'socket': client_socket,
                        'address': address,
                        'nickname': f'User-{address[1]}',
                        'last_active': time.time()
                    }
                    self.clients.append(client_info)
                    
                    # Приветственное сообщение
                    welcome_msg = "Добро пожаловать в чат!\n"
                    client_socket.send(welcome_msg.encode('utf-8'))
                    
                    # Уведомляем всех
                    self.broadcast(f"{client_info['nickname']} присоединился к чату\n")
                    
                    # Запускаем обработчик клиента
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_info,),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue  # Таймаут accept - нормально
                except Exception as e:
                    if self.running:
                        print(f"Ошибка accept: {e}")
                    
        except Exception as e:
            print(f"❌ Ошибка сервера: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_info):
        client_socket = client_info['socket']
        address = client_info['address']
        
        try:
            while self.running:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break  # Клиент отключился
                    
                    client_info['last_active'] = time.time()
                    
                    # Обработка ника
                    if data.startswith('NICK:'):
                        new_nick = data[5:].strip()
                        old_nick = client_info['nickname']
                        client_info['nickname'] = new_nick
                        self.broadcast(f"{old_nick} сменил имя на {new_nick}\n")
                        continue
                    
                    # Обычное сообщение
                    message = data.strip()
                    if message:
                        print(f"📨 {client_info['nickname']}: {message}")
                        self.broadcast(f"{client_info['nickname']}: {message}\n")
                        
                except socket.timeout:
                    continue  # Таймаут - продолжаем
                except Exception as e:
                    print(f"Ошибка чтения от {address}: {e}")
                    break
                    
        except Exception as e:
            print(f"Ошибка обработки клиента {address}: {e}")
        finally:
            self.remove_client(client_info)
    
    def broadcast(self, message):
        """Отправка сообщения всем клиентам"""
        disconnected_clients = []
        
        for client_info in self.clients:
            try:
                client_info['socket'].send(message.encode('utf-8'))
            except:
                disconnected_clients.append(client_info)
        
        # Удаляем отключившихся клиентов
        for client in disconnected_clients:
            self.remove_client(client)
    
    def remove_client(self, client_info):
        if client_info in self.clients:
            self.clients.remove(client_info)
            try:
                client_info['socket'].close()
            except:
                pass
            print(f"❌ Клиент отключен: {client_info['address']}")
            self.broadcast(f"{client_info['nickname']} покинул чат\n")
    
    def cleanup_clients(self):
        """Очистка неактивных клиентов"""
        while self.running:
            time.sleep(10)  # Проверка каждые 10 секунд
            current_time = time.time()
            dead_clients = []
            
            for client_info in self.clients:
                # Если клиент неактивен более 30 секунд
                if current_time - client_info['last_active'] > 30:
                    dead_clients.append(client_info)
            
            for client in dead_clients:
                print(f"🚨 Удален неактивный клиент: {client['address']}")
                self.remove_client(client)
    
    def stop(self):
        self.running = False
        for client_info in self.clients:
            try:
                client_info['socket'].close()
            except:
                pass
        if hasattr(self, 'server_socket'):
            try:
                self.server_socket.close()
            except:
                pass
        print("Сервер остановлен")

if __name__ == '__main__':
    # Автоматическое определение IP
    try:
        host = socket.gethostbyname(socket.gethostname())
    except:
        host = '0.0.0.0'
    
    port = 12345
    
    print(f"IP сервера: {host}")
    print(f"Порт: {port}")
    print("Запуск сервера...")
    print("Для остановки нажмите Ctrl+C")
    
    server = ChatServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.stop()
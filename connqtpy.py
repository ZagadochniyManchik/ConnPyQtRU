from PyQt5 import QtCore, QtGui, QtWidgets
from threading import *
import sys
import socket
import pickle


threads = {}


def pencode(data):
    return pickle.dumps(data)


def pdecode(data):
    return pickle.loads(data)


class ServerObject:
    def __init__(self):
        self.static_data = None
        self.data = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_with(self):
        self.server.connect(('127.0.0.1', 25565))

    def close_with(self):
        self.request(b'CLOSE-CONNECTION')

    def listen_for(self):
        data = self.server.recv(1024)
        while data[:22] != b'<NOTIFICATION-MESSAGE>':
            data = self.server.recv(1024)
        self.notification_handler(data.encode('utf-8'))

    def notification_handler(self, notification):
        message = notification.split(b'<END>')
        getattr(self, message[-1])(message[0])

    def request(self, data):
        self.server.send(data)

    def receive(self):
        # self.data = b''
        # while True:
        #     self.data += self.server.recv(1024)
        #     if self.data[-13:] == b'<END-MESSAGE>':
        #         break
        return pdecode(self.server.recv(1024))


class RegWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.resize(475, 625)
        self.setWindowIcon(QtGui.QIcon('images/icon_photo.png'))

        self.logo_image = QtGui.QPixmap("images/icon_photo.png").scaled(64, 64, QtCore.Qt.KeepAspectRatio)
        self.chat_dark = QtGui.QIcon("images/chat_dark.png")
        self.chat_light = QtGui.QIcon("images/chat_light.png")
        self.theme_dark = QtGui.QIcon("images/theme_dark.png")
        self.theme_light = QtGui.QIcon("images/theme_light.png")

        self.changeTheme_button = QtWidgets.QPushButton('')
        self.changeTheme_button.setIcon(self.theme_dark)
        self.changeTheme_button.clicked.connect(self.change_theme_light)

        self.logo_label = QtWidgets.QLabel('')
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setPixmap(self.logo_image)

        self.layout_logo = QtWidgets.QHBoxLayout()
        self.layout_logo.addWidget(self.logo_label)
        self.layout_logo.addWidget(QtWidgets.QLabel("ConnQtPy"))
        self.layout_logo.addStretch(2)
        self.layout_logo.addWidget(self.changeTheme_button)

        self.widget_for_logo = QtWidgets.QWidget()
        self.widget_for_logo.setLayout(self.layout_logo)

        self.layout = QtWidgets.QVBoxLayout()

        self.login_label = QtWidgets.QLabel("Логин:")
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)

        self.login_input = QtWidgets.QLineEdit()
        self.login_input.setPlaceholderText('Введите логин')

        self.email_label = QtWidgets.QLabel("Эл.Почта:")
        self.email_label.setAlignment(QtCore.Qt.AlignCenter)

        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText('Введите свою эл.почту')

        self.password_label = QtWidgets.QLabel("Пароль:")
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.gender_label = QtWidgets.QLabel("Пол:")
        self.gender_label.setAlignment(QtCore.Qt.AlignCenter)

        self.gender_combo = QtWidgets.QComboBox()
        self.gender_combo.addItems(["Не указано", "Мужчина", "Женщина"])

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)

        self.close_button = QtWidgets.QPushButton("Выйти")
        self.close_button.clicked.connect(lambda: self.close_app())

        self.entryToAccount_label = QtWidgets.QLabel("Уже есть аккаунт?")
        self.entryToAccount_button = QtWidgets.QPushButton("Войти")
        self.entryToAccount_button.clicked.connect(self.login_form)

        self.layout_log_lbl = QtWidgets.QHBoxLayout()
        self.layout_log_lbl.addWidget(self.entryToAccount_label)
        self.layout_log_lbl.addWidget(self.entryToAccount_button)

        self.widget_for_lllb = QtWidgets.QWidget()
        self.widget_for_lllb.setLayout(self.layout_log_lbl)

        self.layout.addWidget(self.widget_for_logo)
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.gender_combo)
        self.layout.addWidget(self.register_button)
        self.layout.addStretch(1)
        self.layout.addWidget(self.widget_for_lllb)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def change_theme_light(self):
        self.setStyleSheet(
            """
            QWidget{
                background: #fff;
                color: #262D37;
            }
            QLineEdit {
                border: 1px solid #262D37;
            }
            QPushButton{
                color: #262D37;
                border: 1px solid #262D37;
            }
            QPushButton:hover{
                background: #ECECEC;
            }
            QComboBox{
                border: 1px solid #262D37;
            }
            """
        )
        self.changeTheme_button.clicked.disconnect()
        self.changeTheme_button.clicked.connect(self.change_theme_dark)
        self.changeTheme_button.setIcon(self.theme_light)

    def change_theme_dark(self):
        self.setStyleSheet(
            """
            QWidget{
                background: #262D37;
                color: #fff;
            }
            QLineEdit {
                border: 1px solid #fff;
            }
            QPushButton{
                color: #fff;
                border: 1px solid #fff;
            }
            QPushButton:hover{
                background: #1E232B;
            }
            QComboBox{
                border: 1px solid #fff;
            }
            """
        )
        self.changeTheme_button.clicked.disconnect()
        self.changeTheme_button.clicked.connect(self.change_theme_light)
        self.changeTheme_button.setIcon(self.theme_dark)

    def register(self):

        login = self.login_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        gender = self.gender_combo.currentText()

        server = ServerObject()
        try:
            server.connect_with()
        except Exception as error:
            print(f'{error}: Check your internet connection')
            QtWidgets.QMessageBox.warning(self, 'Warning', f'{error}: Check your internet connection')
            return
        server.request(
            pencode({"login": login, "email": email, "password": password, "gender": gender})
            + b'<END>' + pencode('<REGISTRATION>') + b'<END>'
        )

        status = server.receive()
        if status != '<SUCCESS>':
            print(status)
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', status)
            return
        QtWidgets.QMessageBox.information(self, 'Информация', 'Аккаунт создан!\nПроизводим вход...')
        server.close_with()

        self.main_window = MainWindow()
        self.destroy()
        self.main_window.show()

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        # server = ServerObject()
        # server.connect_with()
        # server.request(
        #     pencode({"login": login, "password": password}
        #             + b'<END>' + pencode('<LOGIN>') + b'<END>')
        # )
        # server.close_with()

        self.main_window = MainWindow()
        self.destroy()
        self.main_window.show()

    def close_app(self):
        self.close()

    def login_form(self):
        self.email_input.hide()
        self.email_label.hide()
        self.gender_combo.hide()
        self.gender_label.hide()
        self.entryToAccount_button.setText('Зарегистрироваться')
        self.entryToAccount_button.clicked.disconnect()
        self.entryToAccount_button.clicked.connect(self.registration_form)
        self.entryToAccount_label.setText('Нет аккаунта?')
        self.register_button.setText('Войти')
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.login)
        self.setWindowTitle("Вход в аккаунт")

    def registration_form(self):
        self.email_input.show()
        self.email_label.show()
        self.gender_combo.show()
        self.gender_label.show()
        self.entryToAccount_button.setText('Войти')
        self.entryToAccount_button.clicked.disconnect()
        self.entryToAccount_button.clicked.connect(self.login_form)
        self.entryToAccount_label.setText('Уже есть аккаунт?')
        self.register_button.setText('Зарегистрироваться')
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.register)
        self.setWindowTitle("Регистрация")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ConnQtPy")
        self.resize(1280, 720)
        self.setWindowIcon(QtGui.QIcon('images/icon_photo.png'))

        self.central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()

        self.welcome_label = QtWidgets.QLabel('Главный экран')

        self.close_button = QtWidgets.QPushButton("Выйти")
        self.close_button.clicked.connect(self.close_app)

        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.close_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def close_app(self):
        self.close()


def main_thread():
    app = QtWidgets.QApplication(sys.argv)
    style = """
                @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=Prompt:wght@600&display=swap');
                QWidget{
                    background: #262D37;
                    color: #ffffff;
                }
                QHBoxLayout#layout_logo{
                    padding: 10px;
                }
                QComboBox{
                    border: 1px solid #ffffff;
                    border-radius: 8px;
                    font-size: 18px;
                    padding: 10px;
                }
                QPushButton{
                    color: #ffffff;
                    border: 1px solid #ffffff;
                    border-radius: 8px;
                    font-size: 18px;
                    padding: 10px;
                }
                QPushButton:hover{
                    background: #1E232B;
                }
                QPushButton#self.entryToAccount{
                    width: fit-content;
                }
                QLineEdit {
                    color: #ffffff;
                    border: 1px solid #ffffff;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 18px;
                }
                QComboBox{
                    color: #fff;
                }
                QLabel{
                    text-align: center;
                    font-family: 'Franklin Gothic Medium';
                    font-size: 20px;
                }
                QLabel#login_label{
                    background: #fff;
                }
            """
    app.setStyleSheet(style)
    registration_form = RegWindow()
    registration_form.show()
    # main_window = MainWindow()
    # main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main_thr = Thread(target=main_thread(), name='main_thread')
    threads['main_thread'] = main_thr
    main_thr.start()

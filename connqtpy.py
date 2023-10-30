import time

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import *
import sys
import socket
import pickle
import hashlib

threads = {}

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
    background: #262D37;
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
    background: transparent;
}
QLabel#login_label{
    background: #fff;
}
QPushButton#menuButton {
    text-align: left;
    text-padding: 5px;
    font-size: 22px;
    border: 0px transparent; 
    border-radius: 8px;
    background: transparent;
    padding: 20px;
}
QPushButton#menuButton:hover {
    background: #1E232B;
}
QWidget#mainWindow {
    background: #586376;
}
QWidget#profileWidget {
    background: transparent
}
QWidget#messengerWidget {
    background: transparent
}
QWidget#friendsWidget {
    background: transparent
}
QWidget#settingsWidget {
    background: transparent
}
QLabel#titleLabel{
    font-size: 36px
}
QPushButton#logoutButton:hover{
    background: #F83A3A;
    color: #fff;
}
"""


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
        self.request(pencode('None') + b'<END>' + pencode('<CLOSE-CONNECTION>') + b'<END>')

    def listen_for(self):
        while True:
            data = self.server.recv(1024)
            if data == b'<NOTIFICATION-MESSAGE>':
                data = self.server.recv(1024)
                break
        return data

    def request(self, data):
        self.server.send(data)

    def receive(self):
        # self.data = b''
        # while True:
        #     self.data += self.server.recv(1024)
        #     if self.data[-13:] == b'<END-MESSAGE>':
        #         break
        return pdecode(self.server.recv(1024))


class NotificationHandler:
    def __init__(self):
        ...


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
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', status)
            server.close_with()
            return
        QtWidgets.QMessageBox.information(self, 'Информация', 'Аккаунт создан!\nПроизводим вход...')
        server.close_with()

        main_window = MainWindow({"login": login, "email": email, "password": password, "gender": gender})
        self.destroy()
        main_window.show()

    def login(self):
        login = self.login_input.text()
        password = hashlib.sha512(self.password_input.text().encode('utf-8'))

        server = ServerObject()
        try:
            server.connect_with()
        except Exception as error:
            print(f'{error}: Check your internet connection')
            QtWidgets.QMessageBox.warning(self, 'Warning', f'{error}: Check your internet connection')
            return

        server.request(
            pencode({"login": login, "password": password.hexdigest()}) +
            b'<END>' + pencode('<LOGIN>') + b'<END>'
        )

        status = server.receive()
        if status != '<SUCCESS>':
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', status)
            server.close_with()
            return

        QtWidgets.QMessageBox.information(self, 'Информация', 'Входим в аккаунт...')
        server.close_with()

        main_window = MainWindow({'login': login, 'password': password.hexdigest()})
        self.destroy()
        main_window.show()

    def close_app(self):
        self.close_button.hide()
        time.sleep(0.2)
        exit()

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
    def __init__(self, user_data):
        super().__init__()

        self.server = ServerObject()
        self.server.connect_with()
        self.user_data = user_data

        listen_to_server_thr = Thread(target=self.listen_to_server, name='listen_to_server', daemon=True)
        threads['listen_to_server'] = listen_to_server_thr
        listen_to_server_thr.start()

        self.server.request(pencode(self.user_data) + b"<END>" + pencode("<ONLINE>") + b"<END>")

        self.remember_login()

        # !!! Images
        self.logo_image = QtGui.QPixmap("images/icon_photo.png").scaled(80, 80, QtCore.Qt.KeepAspectRatio)
        self.chat_dark = QtGui.QIcon("images/chat_dark.png")
        self.chat_light = QtGui.QIcon("images/chat_light.png")
        self.theme_dark = QtGui.QIcon("images/theme_dark.png")
        self.theme_light = QtGui.QIcon("images/theme_light.png")
        self.friends_dark = QtGui.QIcon("images/add_user_dark.png")
        self.friends_light = QtGui.QIcon("images/add_user_light.png")
        self.profile_light = QtGui.QIcon("images/home_light.png")
        self.profile_dark = QtGui.QIcon("images/home_dark.png")
        self.settings_light = QtGui.QIcon("images/settings_light.png")
        self.settings_dark = QtGui.QIcon("images/settings_dark.png")
        self.exit_light = QtGui.QIcon("images/exit_light.png")
        self.exit_dark = QtGui.QIcon("images/exit_dark.png")
        # !!! Images

        # !!! Window rise
        self.setWindowTitle("ConnQtPy")
        self.resize(1280, 720)
        self.setWindowIcon(QtGui.QIcon('images/icon_photo.png'))

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setObjectName('mainWindow')
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # !!! Menu rise
        self.menu_widget = QtWidgets.QWidget()
        self.menu_widget.setMaximumWidth(400)
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)

        # !!! Menu title rise
        self.title_widget = QtWidgets.QWidget()
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_widget.setLayout(self.title_layout)

        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(self.logo_image)
        self.title_label = QtWidgets.QLabel('\nConnQtPy')
        self.title_label.setStyleSheet('font-size: 30px')

        self.changeTheme_button = QtWidgets.QPushButton()
        self.changeTheme_button.setIcon(self.theme_dark)
        self.changeTheme_button.setMinimumSize(50, 50)
        self.changeTheme_button.clicked.connect(self.change_theme_light)

        self.title_layout.addWidget(self.logo_label)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(1)
        self.title_layout.addWidget(self.changeTheme_button)
        # !!! Menu title end

        # !!! Menu buttons rise
        self.profile_button = QtWidgets.QPushButton('Профиль')
        self.profile_button.setMinimumHeight(50)
        self.profile_button.setIconSize(QtCore.QSize(30, 30))
        self.profile_button.setObjectName('menuButton')
        self.profile_button.clicked.connect(self.show_profile)
        self.profile_button.setIcon(self.profile_light)

        self.messenger_button = QtWidgets.QPushButton('Мессенджер')
        self.messenger_button.setMinimumHeight(50)
        self.messenger_button.clicked.connect(self.show_messenger)
        self.messenger_button.setIcon(self.chat_light)
        self.messenger_button.setIconSize(QtCore.QSize(30, 30))
        self.messenger_button.setObjectName('menuButton')

        self.friends_button = QtWidgets.QPushButton('Друзья')
        self.friends_button.setMinimumHeight(50)
        self.friends_button.clicked.connect(self.show_friends)
        self.friends_button.setIcon(self.friends_light)
        self.friends_button.setIconSize(QtCore.QSize(30, 30))
        self.friends_button.setObjectName('menuButton')

        self.settings_button = QtWidgets.QPushButton('Настройки')
        self.settings_button.setMinimumHeight(50)
        self.settings_button.clicked.connect(self.show_settings)
        self.settings_button.setIcon(self.settings_light)
        self.settings_button.setIconSize(QtCore.QSize(30, 30))
        self.settings_button.setObjectName('menuButton')

        self.close_button = QtWidgets.QPushButton("Выйти")
        self.close_button.clicked.connect(self.close_app)
        self.close_button.setMinimumHeight(50)
        self.close_button.setIcon(self.exit_light)
        self.close_button.setIconSize(QtCore.QSize(30, 30))
        self.close_button.setObjectName('menuButton')

        self.menu_layout.addWidget(self.title_widget)
        self.menu_layout.addStretch(1)
        self.menu_layout.addWidget(self.profile_button)
        self.menu_layout.addWidget(self.messenger_button)
        self.menu_layout.addWidget(self.friends_button)
        self.menu_layout.addWidget(self.settings_button)
        self.menu_layout.addStretch(5)
        self.menu_layout.addWidget(self.close_button)
        # !!! Menu end

        # !!! Menu windows rise
        self.welcome_label = QtWidgets.QLabel('Главный экран')
        self.welcome_label.setStyleSheet('background: transparent')

        # !!! Profile rise
        self.profile_widget = QtWidgets.QWidget()
        self.profile_widget.setObjectName('profileWidget')
        self.profile_layout = QtWidgets.QFormLayout()
        self.profile_widget.setLayout(self.profile_layout)

        self.profileTitle_label = QtWidgets.QLabel('Профиль')
        self.profileTitle_label.setObjectName('titleLabel')
        self.userLogin_label = QtWidgets.QLabel(self.user_data.get('login'))
        self.button = QtWidgets.QPushButton('Example')

        self.profile_layout.addWidget(self.profileTitle_label)
        self.profile_layout.addWidget(self.userLogin_label)
        self.profile_layout.addWidget(self.button)
        # !!! Profile end

        # !!! Messenger rise
        self.messenger_widget = QtWidgets.QWidget()
        self.messenger_widget.setObjectName('messengerWidget')
        self.messenger_layout = QtWidgets.QFormLayout()
        self.messenger_widget.setLayout(self.messenger_layout)

        self.messengerTitle_label = QtWidgets.QLabel('Мессенджер')
        self.messengerTitle_label.setObjectName('titleLabel')

        self.messenger_layout.addWidget(self.messengerTitle_label)
        # !!! Messenger end

        # !!! Friends rise
        self.friends_widget = QtWidgets.QWidget()
        self.friends_widget.setObjectName('friendsWidget')
        self.friends_layout = QtWidgets.QFormLayout()
        self.friends_widget.setLayout(self.friends_layout)

        self.friendsTitle_label = QtWidgets.QLabel('Друзья')
        self.friendsTitle_label.setObjectName('titleLabel')

        self.friends_layout.addWidget(self.friendsTitle_label)
        # !!! Friends end

        # !!! Settings rise
        self.settings_widget = QtWidgets.QWidget()
        self.settings_widget.setObjectName('settingsWidget')
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_widget.setLayout(self.settings_layout)

        self.settingsTitle_label = QtWidgets.QLabel('Настройки')
        self.settingsTitle_label.setObjectName('titleLabel')

        self.logout_button = QtWidgets.QPushButton('Выйти из аккаунта')
        self.logout_button.setMaximumWidth(300)
        self.logout_button.setObjectName('logoutButton')
        self.logout_button.clicked.connect(self.logout)

        self.settings_layout.addWidget(self.settingsTitle_label)
        self.settings_layout.addStretch(1)
        self.settings_layout.addWidget(self.logout_button)
        # !!! Settings end
        # !!! Menu windows end

        self.layout.addWidget(self.menu_widget)
        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.profile_widget)
        self.layout.addWidget(self.messenger_widget)
        self.layout.addWidget(self.friends_widget)
        self.layout.addWidget(self.settings_widget)

        self.profile_widget.hide()
        self.messenger_widget.hide()
        self.friends_widget.hide()
        self.settings_widget.hide()

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        # !!! Window end

    def show_profile(self):
        for window in (self.welcome_label, self.settings_widget, self.friends_widget, self.messenger_widget):
            window.hide()
        self.profile_widget.show()

    def show_messenger(self):
        for window in (self.welcome_label, self.settings_widget, self.friends_widget, self.profile_widget):
            window.hide()
        self.messenger_widget.show()

    def show_friends(self):
        for window in (self.welcome_label, self.settings_widget, self.profile_widget, self.messenger_widget):
            window.hide()
        self.friends_widget.show()

    def show_settings(self):
        for window in (self.welcome_label, self.profile_widget, self.friends_widget, self.messenger_widget):
            window.hide()
        self.settings_widget.show()

    def change_theme_light(self):
        self.setStyleSheet(
            """
QWidget{
    background: #ECECEC;
    color: #262D37;
}
QWidget#mainWindow{
    background: #fff;
}
QLabel {
    background: transparent;
}
QLineEdit {
    border: 1px solid #262D37;
}
QPushButton{
    color: #262D37;
    border: 1px solid #262D37;
}
QPushButton:hover{
    background: #D9D9D9;
}
QComboBox{
    border: 1px solid #262D37;
}
QPushButton#menuButton {
    text-align: left;
    text-padding: 5px;
    border: 0px transparent; 
    border-radius: 8px;
    background: transparent;
}
QPushButton#menuButton:hover {
    background: #D9D9D9;
}
QWidget#profileWidget {
    background: transparent;
}
QWidget#messengerWidget {
    background: transparent
}
QWidget#friendsWidget {
    background: transparent
}
QWidget#settingsWidget {
    background: transparent
}
QPushButton#logoutButton:hover{
    background: #F83A3A;
    color: #fff;
}
""")
        self.changeTheme_button.disconnect()
        self.changeTheme_button.clicked.connect(self.change_theme_dark)
        self.changeTheme_button.setIcon(self.theme_light)
        self.profile_button.setIcon(self.profile_dark)
        self.settings_button.setIcon(self.settings_dark)
        self.messenger_button.setIcon(self.chat_dark)
        self.friends_button.setIcon(self.friends_dark)
        self.close_button.setIcon(self.exit_dark)

    def change_theme_dark(self):
        self.setStyleSheet(style)
        self.setStyleSheet(
            """
QWidget {
    background: #262D37;
}
QWidget#mainWindow{
    background: #586376; 
}
QLabel {
    background: transparent;
}
QPushButton:hover{
    background: #50596A;
}
QPushButton#menuButton:hover{
    background: #1E232B;
}
QWidget#profileWidget {
    background: transparent;
}
QWidget#messengerWidget {
    background: transparent
}
QWidget#friendsWidget {
    background: transparent
}
QWidget#settingsWidget {
    background: transparent
}
QPushButton#logoutButton:hover{
    background: #F83A3A;
    color: #fff;
}
            """
        )
        self.changeTheme_button.disconnect()
        self.changeTheme_button.clicked.connect(self.change_theme_light)
        self.changeTheme_button.setIcon(self.theme_dark)
        self.profile_button.setIcon(self.profile_light)
        self.settings_button.setIcon(self.settings_light)
        self.messenger_button.setIcon(self.chat_light)
        self.friends_button.setIcon(self.friends_light)
        self.close_button.setIcon(self.exit_light)

    def listen_to_server(self):
        while True:
            status = self.server.listen_for()
            self.notification_handler(status)

    def notification_handler(self, notification):
        message = notification.split(b'<END>')[:-1]
        getattr(self, pdecode(message[-1]))(pdecode(message[0]))

    def remember_login(self):
        with open('static/lastlogin.txt', 'wb') as file:
            file.write(b'True\n')
            file.write(pencode(self.user_data))

    def logout(self):
        self.server.request(pencode(self.user_data) + b"<END>" + pencode("<OFFLINE>") + b"<END>")
        self.server.close_with()
        with open('static/lastlogin.txt', 'wb') as file:
            file.write(b'False\n')
        reg_form = RegWindow()
        time.sleep(0.2)
        self.destroy()
        reg_form.show()

    def close_app(self):
        self.server.request(pencode(self.user_data) + b"<END>" + pencode("<OFFLINE>") + b"<END>")
        self.server.close_with()
        time.sleep(0.2)
        exit()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.server.request(pencode(self.user_data) + b"<END>" + pencode("<OFFLINE>") + b"<END>")
        self.server.close_with()
        time.sleep(0.2)
        exit()


def last_login():
    data = []
    with open('static/lastlogin.txt', 'rb') as file:
        data.extend(file.readlines())
    if data[0] == b'True\n':
        return pdecode(data[-1])
    else:
        return None


def main_thread():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style)
    status = last_login()
    if status is None:
        registration_form = RegWindow()
        registration_form.show()
    else:
        main_window = MainWindow(status)
        main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main_thr = Thread(target=main_thread(), name='main_thread', daemon=True)
    threads['main_thread'] = main_thr
    main_thr.start()
    exit()

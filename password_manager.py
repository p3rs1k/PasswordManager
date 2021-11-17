from cryptography.fernet import Fernet, InvalidToken
import os.path


class KeyLoader:
    def __init__(self):
        self.key = str()
        if not os.path.isfile('key.key'):
            self._write_key()
        else:
            self.load_key()

    def _write_key(self):
        with open('key.key', 'wb') as key_file:
            self.key = Fernet.generate_key()
            key_file.write(self.key)

    def load_key(self):
        with open('key.key') as key_file:
            self.key = key_file.read()
        return self.key


class PasswordMAnager(KeyLoader):
    def __init__(self):
        super().__init__()
        self.fer = Fernet(self.key)

    def add(self):
        name = input('Enter your name: ')
        pwd = input('Enter your pwd: ')

        with open('passwords.txt', 'a') as f:
            f.write(f"{name}|{self.fer.encrypt(pwd.encode()).decode()}\n")

    def view(self):
        with open('passwords.txt') as f:
            data = f.readlines()
        try:
            print("Name | Password")
            for i in data:
                name, pwd = i.split('|')
                print(f"{name} | {self.fer.decrypt(pwd.encode()).decode()}")
        except InvalidToken:
            print("Invalid Token")


if __name__ == '__main__':
    pm = PasswordMAnager()

    while True:
        flag = input('Enter (add/view or q to quit) ').lower()
        if flag == 'q':
            break
        elif flag == 'add':
            pm.add()
        elif flag == 'view':
            pm.view()
        else:
            print('Do it again')

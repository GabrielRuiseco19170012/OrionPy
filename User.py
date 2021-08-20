from os import system, name as sysname

class User:

    def __init__(self):
        self.id = None
        self.email = "mail@mail.com"
        self.password = "password1"
        self.token = ""
        self.type = 'bearer'

    def saveToken(self, newToken):
        self.token = newToken

    def getToken(self):
        return self.token

    def saveID(self, newID):
        self.id = newID

    def getID(self):
        return self.id

    @staticmethod
    def clear():
        # for windows
        if str(sysname) == "nt":
            _ = system("cls")
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system("clear")

    def saveData(self):
        User.clear()
        email = input("Ingrese el correo del usuario: ")
        password = input("Ingrese la contraseña del usuario: ")
        self.email = email
        self.password = password

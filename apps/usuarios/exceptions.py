class InvalidFieldException(Exception):
    def __init__(self, message):
        self.message = message

class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = 'Já existe um usuário cadastrado com esse email.'

class SendMailException(Exception):
    def __init__(self):
        self.message = 'Erro ao enviar email.'
        
class AuthenticationException(Exception):
    def __init__(self):
        self.message = 'Login e/ou senha inválidos.'
        
class UserCannotBeDeletedException(Exception):
    def __init__(self):
        self.message = 'Este usuário não pode ser deletado.'
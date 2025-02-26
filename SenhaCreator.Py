import random
import string
import hashlib
import os
import base64
from datetime import datetime

class PasswordGenerator:
    def __init__(self, length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True, avoid_repeating=True):
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_special = use_special
        self.avoid_repeating = avoid_repeating
        
        self.char_sets = {
            'upper': string.ascii_uppercase,
            'lower': string.ascii_lowercase,
            'digits': string.digits,
            'special': string.punctuation
        }
    def generate_base_charset(self):
        """
        Cria o conjunto de caracteres baseados nas opções de configuração.
        """
        char_set = ""
        if self.use_upper:
            char_set += self.char_sets['upper']
        if self.use_lower:
            char_set += self.char_sets['lower']
        if self.use_digits:
            char_set += self.char_sets['digits']
        if self.use_special:
            char_set += self.char_sets['special']
        return char_set
    def generate_password_avoid_repeating(self):
        """
        Gera uma senha única sem caracteres repetidos.
        """
        char_set = self.generate_base_charset()
        if len(char_set) < self.length:
            raise ValueError("O conjunto de caracteres é menor que o tamanho da senha.")
        password = ''.join(random.sample(char_set, self.length))
        return password
    def hash_password(self, password):
        """
        Gera o hash da senha utilizando o algoritmo SHA-256 com salt.
        """
        salt = os.urandom(16) # Gerando um salt aleatório
        password_bytes = password.encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
        hashed_password = base64.b64decode(hashed).decode('utf-8')
        return hashed_password
    def password_strength(self, password):
        """
        Avalia a força de uma senha com base em seu comprimento e variedade de caracteres.
        """
        score = 0
        if len(password) >= 12:
            score +=1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
            if any(c in string.punctuation for c in password):
                score +=1
            return score
    def save_password(self, password):
        filename = "passwords.txt"
        with open(filename, "a") as file:
            file.write(f"{datetime.now()}: {password}\n")
        return f"Senha salva no arquivo {filename}"
    def display_summary(self):
        """
        Exibe um resumo das configurações e status do gerador.
        """
        print("Resumo da coniguração do gerador de senha:")
        print(f"Comprimento da senha: {self.length}")
        print(f"usar letras maiúsculas: {'Sim' if self.use_upper else 'Não'}")
        print(f"Usar letras minúsculas: {'Sim' if self.use_lower else 'Não'}")
        print(f"Usar caracteres especiais: {'Sim' if self.use_special else 'Não'}")
        print(f"Evitar caracteres repetidos: {'Sim' if self.avoid_repeating else 'Não'}")
        print(f"Usar números: {'Sim' if self.use_digits else 'Não'}")
    def set_length(self, length):
        self.length = length
    def set_use_upper(self, use_upper):
        self.use_upper = use_upper
    def set_use_lower(self, use_lower):
        self.use_lower = use_lower
    def set_use_digits(self, use_digits):
        self.use_digits = use_digits
    def set_use_special(self, use_special):
        self.use_special(self, use_special)
    def set_avoid_repeating(self, avoid_repeating):
        self.avoid_repeating = avoid_repeating
        
    def main(self):
        print("Bem-vindo ao gerador de senhas complexas!")
        print("Escolha as configurações para gerar sua senha. \n")
        
        while True:
            self.display_summary()
            action = input("\nEscolha uma opção:\n1 - Gerar senha \n2 - Verificar força da senha\n3 - Salvar\n4 - Sair\n ")
            
            if action == '1':
                if self.avoid_repeating:
                    Password = self.generate_password_avoid_repeating()
                else:
                    Password = self.generate_base_charset()
                print(f"Senha gerada: {Password}")
            elif action == '2':
                Password = input("Digite a senha para verificar a força:")
                strength = self.password_strength(Password)
                print(f"Força da senha: {strength}")
            elif action == '3':
                Password_to_save = input("Digite a senha para salvar: ")
                print(self.save_password(Password_to_save))
            elif action == '4':
                print("Saindo...Até logo :)")
                break
            else:
                print("Opção inválida")
                
if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.main()
    
import numpy as np
import re
import string

from unidecode import unidecode


AZ = string.ascii_lowercase  # Alphabet lowercase letters
ALF_TO_DEC = {AZ[i] : i for i in range(26)}  # Maps alphabetical to decimal
DEC_TO_ALF = {i : AZ[i] for i in range(26)}  # Maps decimal to alphabetical


# Function from GeraEP1.py script to read and parse public text
def parse_file(file_name):
    
    with open(file_name, 'r', encoding='utf8', errors='ignore') as input_file:  # Fix: set encoding and errors args to prevent exceptions
        file_content = input_file.read()

    file_content = file_content.lower()
    file_content = unidecode(file_content)
    file_content = re.sub(r'[^a-z]', '', file_content)
    
    return file_content


# Uses the public text and the 2 ciphers to find the key thus decrypting both ciphers
def brute_force_decrypt(public_text: str, cipher: list):
    cipher_1 = cipher[0]
    cipher_2 = cipher[1]

    decimal_cipher_1 = [ALF_TO_DEC[k] for k in cipher_1]
    decimal_cipher_2 = [ALF_TO_DEC[k] for k in cipher_2]

    chunk_size = len(cipher_1)
    
    # Iterates over public text
    for i in range(len(public_text) - chunk_size):
        base_chunk = public_text[i:chunk_size + i]

        decimal_base_chunk = [ALF_TO_DEC[k] for k in base_chunk]

        # To decrypt:                     (cipher_text - key) % 26 = plain_text
        # To get the key used to decrypt: key = (cipher_text - plain_text) % 26
        decrypt_key = ( np.array(decimal_cipher_1) - np.array(decimal_base_chunk) ) % 26

        plain_text = ( np.array(decimal_cipher_2) - decrypt_key ) % 26
        plain_text = [DEC_TO_ALF[k] for k in plain_text]
        plain_text = ''.join(plain_text)

        if re.search(r'(?:(?![aeiou])[a-z]){5,}', plain_text) is None:  # Checks if there's 5 consonants or more sequentially in the plain text decrypted

            # Iterates again over the public text, starting at the next letter after base_chunk until the last chunk available
            for j in range(chunk_size + i, len(public_text) - chunk_size):
                movable_chunk = public_text[j:chunk_size + j]

                if plain_text in movable_chunk:
                    decrypt_key = [DEC_TO_ALF[k] for k in decrypt_key]
                    decrypt_key = ''.join(decrypt_key)

                    print("DECODED MESSAGE")
                    print(f"Cipher 1: {cipher_1} decodes: {base_chunk}")
                    print(f"Cipher 2: {cipher_2} decodes: {movable_chunk}")
                    print(f"Key used: {decrypt_key}")


public_text = parse_file('ExercicioPrograma\EP_solucao\policarpo_quaresma.txt')

ciphers = []

with open('ExercicioPrograma\EP_Seguranca_informacao\Texto_conhecido\Cifrado\Vigenere\Grupo07_texto_cifrado1.txt', 'r') as cipher_file:
    ciphers.append(cipher_file.read())

with open('ExercicioPrograma\EP_Seguranca_informacao\Texto_conhecido\Cifrado\Vigenere\Grupo07_texto_cifrado2.txt', 'r') as cipher_file:
    ciphers.append(cipher_file.read())

brute_force_decrypt(public_text=public_text, cipher=ciphers)
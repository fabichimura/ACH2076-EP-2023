import numpy as np
import re
import string

from unidecode import unidecode


AZ = string.ascii_lowercase  # Alphabet lowercase letters


# Function from GeraEP1.py script to read and parse public text
def parse_file(file_name):
    
    with open(file_name, 'r', encoding='utf8', errors='ignore') as input_file:  # Fix: set encoding and errors args to prevent exceptions
        file_content = input_file.read()

    file_content = file_content.lower()
    file_content = unidecode(file_content)
    file_content = re.sub(r'[^a-z]', '', file_content)
    
    return file_content
     

# Returns True if the key is at least 2/3 different then alphabet
def is_valid_key(key: str):
    counter = 0

    for i in range(len(key)):
        if key[i] == AZ[i]:
            counter += 1
    
    if counter > 9:  # 26 / 3 rounded up
        return False
    
    return True


# Returns next key permutation
def generate_next_key(key: str):
    numeric_key = [AZ.index(key[i]) for i in range(26)]
    
    next_permutation(numeric_key)

    return ''.join([AZ[numeric_key[i]] for i in range(26)])


# Swap element positions in a list
def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
 

# Function to find the next permutation - algorithm found in https://www.geeksforgeeks.org/next-permutation/
def next_permutation(arr):
    n = len(arr)
    i = 0
    j = 0
     
    # Find for the pivot element.
    # A pivot is the first element from
    # end of sequencewhich doesn't follow
    # property of non-increasing suffix
    for i in range(n-2, -1, -1):
        if (arr[i] < arr[i + 1]):
            break
             
    # Check if pivot is not found
    if (i < 0):
        arr.reverse()
 
    # if pivot is found
    else:
        # Find for the successor of pivot in suffix
        for j in range(n-1, i, -1):
            if (arr[j] > arr[i]):
                break
 
        # Swap the pivot and successor
        swap_positions(arr, i, j)
         
        # Minimise the suffix part
        # initializing range
        strt, end = i+1, len(arr)
 
        # Third arg. of split with -1 performs reverse
        arr[strt:end] = arr[strt:end][::-1]


# Attempts to decrypt a given cipher using a given decrypt key. To make sure the decryption went well, checks if the plain open text generated thoughout the decryption process is present in the given public text
async def decrypt(decrypt_key: str, public_text: str, cipher: str):

    decript_key_map = {decrypt_key[i] : AZ[i] for i in range(26)}
    
    plain_text = [decript_key_map[i] for i in cipher]
    plain_text = ''.join(plain_text)

    if plain_text in public_text:
        print(f"KEY FOUND: {decrypt_key}")
        print(f"DECODED MESSAGE: {plain_text}")

        return True
    return False


# Approach 1: pure brute force, starts with a given key and if the decryption hasn't succeeded, attempts to decrypt again using the next valid key permutation available
async def brute_force_decrypt_1(key: str, public_text: str, cipher: str):
    while(not decrypt(decrypt_key=key, public_text=public_text, cipher=cipher)):
        key = generate_next_key(key)


# Approach 2: again, pure brute force. But instead of using the next valid key permutation available, it ramdonly chooses a new permutation
async def brute_force_decrypt_2(key: str, public_text: str, cipher: str):
    while(not decrypt(decrypt_key=key, public_text=public_text, cipher=cipher)):
        key = np.random.permutation(26)
        key = ''.join([AZ[key[i]] for i in range(26)])


# Approach 3: uses the public text and the cipher to find the key thus decrypting the given cipher
def brute_force_decrypt_3(public_text: str, cipher: str):
    chunk_size = len(cipher)
    plain_text = list("*" * chunk_size)
    
    # Iterate over public text
    for i in range(len(public_text) - chunk_size):
        chunk = public_text[i:chunk_size + i]

        # if i % (chunk_size * 10) == 0:
        #     print(chunk)

        # Iterate over cipher
        for j in range(chunk_size):
            letter_j_index_list = [k for k, letter in enumerate(cipher) if letter == cipher[j]]

            is_decrypt_working = True
            
            for index in letter_j_index_list:

                if chunk[index] == chunk[j]:
                    plain_text[index] = chunk[j]
                else:
                    is_decrypt_working = False
                    break

            if not is_decrypt_working:
                break

        if "*" not in plain_text:
            plain_text = ''.join(plain_text)
            print(f"DECODED MESSAGE: {plain_text}")

            return plain_text


key = 'abcdefghiklmnopqrstuvwxyzj' # First valid permutation key
public_text = parse_file('ExercicioPrograma\EP_solucao\policarpo_quaresma.txt')
# public_text = parse_file('policarpo_quaresma.txt')

with open('ExercicioPrograma\EP_Seguranca_informacao\Texto_conhecido\Cifrado\Mono\Grupo07_texto_cifrado.txt', 'r') as cipher_file:
# with open('C:\Users\Raphael\Documents\Rapha\USP\Seguranca da Informacao\EP\ExercicioPrograma\EP_Seguranca_informacao\Texto_conhecido\Cifrado\Mono\Grupo07_texto_cifrado.txt', 'r', encoding='utf8') as cipher_file:
    cipher = cipher_file.read()

# brute_force_decrypt_1(key=key, public_text=public_text, cipher=cipher)

# key = np.random.permutation(26)
# key = ''.join([AZ[key[i]] for i in range(26)])

# brute_force_decrypt_2(key=key, public_text=public_text, cipher=cipher)

brute_force_decrypt_3(public_text=public_text, cipher=cipher)
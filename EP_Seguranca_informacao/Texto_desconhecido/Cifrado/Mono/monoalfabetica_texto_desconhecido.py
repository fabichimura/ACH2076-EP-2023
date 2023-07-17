import itertools
import re
import string

from unidecode import unidecode


AZ = string.ascii_lowercase  # Alphabet lowercase letters

PTBR_LETTER_FREQUENCIES = {'a': 14.63, 'e': 12.57, 'o': 10.73, 's': 7.81, 'r': 6.53, 'i': 6.18, 'n': 5.05, 'd': 4.99, 'm': 4.74, 'u': 4.63, 't': 4.34, 'c': 3.88, 'l': 2.78, 'p': 2.52, 'v': 1.67, 'g': 1.3, 'h': 1.28, 'q': 1.2, 'b': 1.04, 'f': 1.02, 'z': 0.47, 'j': 0.4, 'x': 0.21, 'k': 0.02, 'w': 0.01, 'y': 0.01}

PTBR_BIGRAM_FREQUENCIES = {'de': 1.76, 'ra': 1.67, 'es': 1.65, 'os':1.51, 'as':1.49, 'do': 1.41, 'ar': 1.33, 'co': 1.31, 'en': 1.23, 'qu': 1.2, 'er': 1.18, 'da': 1.17, 're': 1.14, 'ca': 1.11, 'ta': 1.1, 'se': 1.08, 'nt': 1.08, 'ma': 1.06, 'ue': 1.05, 'te': 1.05}

PTBR_TRIGRAM_FREQUENCIES = {'que': 0.96, 'ent': 0.56, 'com': 0.47, 'nte': 0.44, 'est': 0.34, 'ava': 0.34, 'ara': 0.33, 'ado': 0.33, 'par': 0.3, 'ndo': 0.3, 'nao': 0.3, 'era': 0.3, 'and': 0.3, 'uma': 0.28, 'sta': 0.28, 'res': 0.27, 'men': 0.27, 'con': 0.27, 'dos': 0.25, 'ant': 0.25}

PTBR_NON_FINAL_LETTERS = ['d', 't', 'h', 'n', 'c', 'y', 'b', 'x', 'v', 'k', 'g', 'f', 'p', 'w', 'q', 'j']

PTBR_1_LETTER_WORDS = ['a', 'e', 'o']

# From https://www.palavras.net/
PTBR_2_LETTER_WORDS = ['es', 'ao', 'as', 'xa', 'xi', 've', 'va', 'va', 'vi', 'ue', 'um', 'ui', 'uh', 'te', 'tu', 'ti', 'te', 'so', 'se', 'se', 'sa', 'si', 'se', 'ra', 'ri', 'po', 'pe', 'pa', 'ou', 'os', 'oi', 'oh', 'nu', 'no', 'no', 'na', 'ma', 'mo', 'me', 'ma', 'le', 'la', 'la', 'lo', 'li', 'la', 'ja', 'ir', 'ih', 'ia', 'ha', 'fe', 'fa', 'ex', 'eu', 'em', 'do', 'de', 'da', 'do', 'de', 'da', 'ca', 'cu', 'ai', 'as', 'ar', 'ao', 'ai', 'ah', 'ze', 'tv', 'sa', 'im', 'bc', 'ac']

# From https://www.palavras.net/
PTBR_3_LETTER_WORDS = ['ima', 'zen', 'voo', 'vos', 'ves', 'vem', 'veu', 'vas', 'vao', 'vas', 'voa', 'voz', 'vou', 'vos', 'voe', 'voa', 'via', 'viu', 'vis', 'vir', 'vim', 'vil', 'vii', 'via', 'vez', 'ver', 'vem', 'vai', 'uva', 'usa', 'uso', 'use', 'usa', 'uns', 'uno', 'uni', 'une', 'una', 'uma', 'uai', 'tem', 'tao', 'tua', 'tom', 'tio', 'tia', 'tez', 'teu', 'ter', 'tem', 'tal', 'soo', 'sos', 'sas', 'sua', 'suo', 'sue', 'sub', 'sua', 'soa', 'sou', 'som', 'sol', 'soe', 'sob', 'soa', 'sim', 'seu', 'ser', 'sem', 'sei', 'sai', 'sal', 'sai', 'roo', 'roi', 'res', 'reu', 'res', 'rum', 'rui', 'rua', 'roi', 'roe', 'roe', 'roa', 'riu', 'ris', 'rir', 'rim', 'ria', 'rei', 'que', 'poe', 'pos', 'por', 'pos', 'pes', 'pao', 'pas', 'pus', 'pua', 'pro', 'pre', 'pro', 'pra', 'por', 'pia', 'pio', 'pie', 'pia', 'per', 'paz', 'pau', 'par', 'ovo', 'ora', 'oro', 'ore', 'ora', 'opo', 'opa', 'ola', 'ois', 'ode', 'oco', 'oca', 'oba', 'nus', 'nos', 'nao', 'num', 'nua', 'noz', 'nos', 'nem', 'nas', 'moo', 'moi', 'mes', 'mao', 'mae', 'mas', 'mui', 'moi', 'moe', 'mos', 'mor', 'moe', 'moa', 'mia', 'mio', 'mim', 'mil', 'mie', 'mia', 'meu', 'mel', 'mau', 'mas', 'mal', 'les', 'leu', 'las', 'luz', 'lua', 'los', 'lia', 'lho', 'lhe', 'lha', 'leu', 'ler', 'lei', 'las', 'lar', 'jus', 'jaz', 'ica', 'ico', 'ica', 'ira', 'ira', 'ido', 'ide', 'ida', 'ice', 'ias', 'iam', 'hao', 'has', 'hum', 'hem', 'hei', 'gas', 'gol', 'gnu', 'giz', 'gil', 'gea', 'fas', 'fui', 'foz', 'for', 'foi', 'fia', 'fiz', 'fio', 'fim', 'fie', 'fia', 'faz', 'etc', 'era', 'els', 'elo', 'ele', 'ela', 'eis', 'eia', 'ego', 'eco', 'doo', 'doi', 'des', 'dao', 'das', 'duo', 'dum', 'doi', 'doe', 'doa', 'dou', 'dos', 'dor', 'dom', 'doe', 'doa', 'diz', 'dia', 'dez', 'deu', 'der', 'dei', 'dai', 'das', 'dar', 'dai', 'coo', 'ceu', 'cao', 'cus', 'cru', 'cre', 'cri', 'coa', 'cor', 'com', 'coe', 'coa', 'cla', 'cio', 'cha', 'cha', 'cea', 'cem', 'cai', 'cal', 'cai', 'bom', 'boi', 'boa', 'bit', 'bis', 'bem', 'bel', 'bau', 'bar', 'aco', 'azo', 'avo', 'avo', 'ave', 'ate', 'ate', 'ata', 'ato', 'ate', 'ata', 'asa', 'ara', 'aro', 'are', 'ara', 'aos', 'ana', 'ano', 'ama', 'amo', 'ame', 'ama', 'alo', 'ali', 'ala', 'ajo', 'aja', 'ais', 'aia', 'agi', 'age', 'afa', 'adi', 'aba', 'sao', 'sul', 'sbm', 'rio', 'pai', 'ohm', 'mar', 'mdc', 'ira', 'ibm', 'hiv', 'gra', 'fez', 'eva', 'ema', 'eua', 'ana', 'ala']

VOWELS = ['a', 'e', 'i', 'o', 'u']

# From https://www.palavras.net/
PTBR_2_LETTER_PERMUTATIONS = [
	['a', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'ax', 'az'],
    ['b', 'ba', 'bd', 'be', 'bi', 'bj', 'bl', 'bm', 'bo', 'br', 'bs', 'bt', 'bu', 'bv'],
    ['c', 'ca', 'cc', 'ce', 'ch', 'ci', 'cl', 'cn', 'co', 'cr', 'ct', 'cu'],
    ['d', 'da', 'de', 'di', 'dj', 'dm', 'do', 'dr', 'du', 'dv'],
    ['e', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'el', 'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ex', 'ey', 'ez'],
    ['f', 'fa', 'fe', 'fi', 'fl', 'fo', 'fr', 'ft', 'fu'],
    ['g', 'ga', 'ge', 'gi', 'gl', 'gm', 'gn', 'go', 'gr', 'gt', 'gu'],
    ['h', 'ha', 'he', 'hi', 'ho', 'hu'],
    ['i', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'ix', 'iz'],
    ['j', 'ja', 'je', 'ji', 'jo', 'ju'],
    ['k'],
    ['l', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'll', 'lm', 'ln', 'lo', 'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lx', 'lz'],
    ['m', 'ma', 'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mx', 'mz'],
    ['n', 'na', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nl', 'no', 'nq', 'nr', 'ns', 'nt', 'nu', 'nv', 'nx', 'nz'],
    ['o', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi', 'oj', 'ok', 'ol', 'om', 'on', 'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou', 'ov', 'ox', 'oz'],
    ['p', 'pa', 'pc', 'pe', 'ph', 'pi', 'pl', 'pn', 'po', 'pr', 'ps', 'pt', 'pu'],
    ['q', 'qu'],
    ['r', 'ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rl', 'rm', 'rn', 'ro', 'rp', 'rq', 'rr', 'rs', 'rt', 'ru', 'rv', 'rx', 'rz'],
    ['s', 'sa', 'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sl', 'sm', 'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sx', 'sz'],
    ['t', 'ta', 'tc', 'te', 'ti', 'tm', 'tn', 'to', 'tr', 'ts', 'tu', 'tv'],
    ['u', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui', 'uj', 'ul', 'um', 'un', 'uo', 'up', 'uq', 'ur', 'us', 'ut', 'uu', 'uv', 'ux', 'uz'],
    ['v', 'va', 've', 'vi', 'vo', 'vr', 'vu'],
    ['w'],
    ['x', 'xa', 'xc', 'xe', 'xi', 'xo', 'xp', 'xt', 'xu'],
    ['y'],
    ['z', 'za', 'zb', 'zc', 'zd', 'ze', 'zf', 'zg', 'zh', 'zi', 'zj', 'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zx', 'zz']
]

PLAIN_TEXT = list('*' * 100)

DECRYPT_KEY = {letter : '*' for letter in AZ}

CONFIDENCE_INTERVAL = 5


# Function from GeraEP1.py script to read and parse public text
def parse_file(file_name):
    
    with open(file_name, 'r', encoding='utf8', errors='ignore') as input_file:  # Fix: set encoding and errors args to prevent exceptions
        file_content = input_file.read()

    file_content = file_content.lower()
    file_content = unidecode(file_content)
    file_content = re.sub(r'[^a-z]', '', file_content)
    
    return file_content
     

def analyze_cipher_text(cipher_text: str):
    # Inspects the received cipher text to retrive letter frequencies
    letter_frequency_mapping = {AZ[i] : cipher_text.count(AZ[i]) for i in range(len(AZ))}
    letter_frequency_mapping = {key : val for key, val in letter_frequency_mapping.items() if val > 0}

    # Inspects the received cipher text to determine letter sociability (more sociable letters are usually vowels)
    letter_sociability_mapping = {}

    for letter in AZ:
    
        letter_sociability = []

        for i in range(len(cipher_text)):
            if letter == cipher_text[i]:
                letter_sociability.append(cipher_text[i - 1 if i > 0 else i + 1])
                letter_sociability.append(cipher_text[i + 1 if i < len(cipher_text) - 1 else i - 1])

        letter_sociability_mapping[letter] = len(set(letter_sociability))

    letter_sociability_mapping = {key : val for key, val in letter_sociability_mapping.items() if val > 0}

    # Inspects the received cipher text to find the most frequent bigrams
    bigram_mapping = {''.join([cipher_text[i], cipher_text[i + 1]]) : cipher_text.count(''.join([cipher_text[i], cipher_text[i + 1]])) for i in range(len(cipher_text) - 1)}
    bigram_mapping = {key : val for key, val in bigram_mapping.items() if val > 1}

    # Inspects the received cipher text to find the most frequent trigrams
    trigram_mapping = {''.join([cipher_text[i], cipher_text[i + 1], cipher_text[i + 2]]) : cipher_text.count(''.join([cipher_text[i], cipher_text[i + 1], cipher_text[i + 2]])) for i in range(len(cipher_text) - 2)}
    trigram_mapping = {key : val for key, val in trigram_mapping.items() if val > 1}

    # Sorts all mappings descending
    letter_frequency_mapping = dict(sorted(letter_frequency_mapping.items(), key=lambda x : x[1], reverse=True))
    letter_sociability_mapping = dict(sorted(letter_sociability_mapping.items(), key=lambda x : x[1], reverse=True))
    bigram_mapping = dict(sorted(bigram_mapping.items(), key=lambda x : x[1], reverse=True))
    trigram_mapping = dict(sorted(trigram_mapping.items(), key=lambda x : x[1], reverse=True))

    return [letter_frequency_mapping, letter_sociability_mapping, bigram_mapping, trigram_mapping]


def candidate_letter_mappings(cipher_letter: str) -> list:
    cipher_letter_frequency_index = list(cipher_text_mappings[0].keys()).index(cipher_letter)
    cipher_letter_sociability_index = list(cipher_text_mappings[1].keys()).index(cipher_letter)
    related_bigrams = []
    related_trigrams = []

    for bigram in cipher_text_mappings[2]:
        if cipher_letter in bigram:
            related_bigrams.append(bigram)

    for trigram in cipher_text_mappings[3]:
        if cipher_letter in trigram:
            related_trigrams.append(trigram)
    
    letter_frequency_candidates = []
    letter_sociability_candidates = []
    ptbr_frequency_list = list(PTBR_LETTER_FREQUENCIES.keys())

    for i in range(CONFIDENCE_INTERVAL):
        positive_index = cipher_letter_frequency_index + i
        negative_index = cipher_letter_frequency_index - i
        letter_frequency_candidates.append(ptbr_frequency_list[positive_index if positive_index < len(ptbr_frequency_list) - 1 else cipher_letter_frequency_index])
        letter_frequency_candidates.append(ptbr_frequency_list[negative_index if negative_index >= 0 else cipher_letter_frequency_index])
        positive_index = cipher_letter_sociability_index + i
        negative_index = cipher_letter_sociability_index - i
        letter_sociability_candidates.append(ptbr_frequency_list[positive_index if positive_index < len(ptbr_frequency_list) - 1 else cipher_letter_sociability_index])
        letter_sociability_candidates.append(ptbr_frequency_list[negative_index if negative_index >= 0 else cipher_letter_sociability_index])

    letter_frequency_candidates.extend(letter_sociability_candidates)
    letter_candidates = list(set(letter_frequency_candidates))
    letter_candidates = sorted(letter_candidates, key=lambda x : PTBR_LETTER_FREQUENCIES[x], reverse=True)

    return [letter_candidates, related_bigrams, related_trigrams]


def erase_decrypt_attempt(plain_text: list, index_list: list):
    for index in index_list:
        plain_text[index] = '*'


def decrypt_bigrams_trigrams(related_bigram_trigram: list):
    decrypted_bigram_trigram = []
    local_decrypt_key = {}
    
    for key in DECRYPT_KEY:
        if DECRYPT_KEY[key] != '*':
            local_decrypt_key[DECRYPT_KEY[key]] = key

    for bigram_trigram in related_bigram_trigram:
        decrypted_bigram_trigram.append(''.join([local_decrypt_key[i] if i in local_decrypt_key else '*' for i in bigram_trigram]))

    return [bigram_trigram for bigram_trigram in decrypted_bigram_trigram if '*' not in bigram_trigram]


def is_consistent(slice=[], bigrams=[], trigrams=[]):

    if bigrams:
        for bigram in bigrams:
            if bigram not in PTBR_2_LETTER_PERMUTATIONS[AZ.index(bigram[0])] and bigram not in PTBR_BIGRAM_FREQUENCIES:
                return False
    
    if trigrams:
        for trigram in trigrams:
            for j in range(2):
                if trigram[j:j + 2] not in PTBR_2_LETTER_PERMUTATIONS[AZ.index(trigram[j])]:
                    return False
            # if trigram not in PTBR_TRIGRAM_FREQUENCIES and trigram not in PTBR_3_LETTER_WORDS:
            #     return False

    if slice:
        if len(slice) >= 2:  # Checks if bigrams are consistent according to ptbr possible 2 letter permutations
            for i in range(len(slice) - 1):
                if slice[i:i + 2] not in PTBR_2_LETTER_PERMUTATIONS[AZ.index(slice[i])]:
                    return False

            consonant_counter = len(re.findall(r'[^aeiou]{5}', slice))
            vowel_counter = len(re.findall(r'[aeiou]{7}', slice))

            if consonant_counter > 0 or vowel_counter > 0:
                return False

    return True


def save_decrypt_attempt():
    with open('mono_decrypt_attempt.txt', 'a') as file:
        file.write(f"Counter: {counter}\nPlain Text: {''.join(PLAIN_TEXT)}\nDecrypt Key: {DECRYPT_KEY}\n")
    print("File saved successfully")
    print("Cypher cracked!!!")
    print(f"Plain text: {''.join(PLAIN_TEXT)}\nDecrypt key: {DECRYPT_KEY}")


def generate_decrypt_key() -> bool:
  
    # Gets next available cipher letter
    for cipher_letter in cipher_text_mappings[0]:
        if cipher_letter not in DECRYPT_KEY.values():
            break

    cipher_letter_index_list = [k for k, letter in enumerate(cipher_text) if letter == cipher_letter]

    # Checks the candidate letters that the given cipher letter can decrypt to considering the confidence interval. The Candidate Letter Mappings function returns a list of three elements. The first one is a list of candidate letters, ordered by PTBR_LETTER_FREQUENCY. The second one is a list of related bigrams whereas the third one is a list of related trigrams
    candidate_letters_bigrams_trigrams = candidate_letter_mappings(cipher_letter)

    for candidate_letter in candidate_letters_bigrams_trigrams[0]:

        if DECRYPT_KEY[candidate_letter] != '*':
            pass

        elif candidate_letter in VOWELS and cipher_text_mappings[1][cipher_letter] < sociability_average:
            pass

        else:
            DECRYPT_KEY[candidate_letter] = cipher_letter

            for index in cipher_letter_index_list:
                PLAIN_TEXT[index] = candidate_letter

            candidate_letters_bigrams_trigrams[1] = decrypt_bigrams_trigrams(candidate_letters_bigrams_trigrams[1])
            candidate_letters_bigrams_trigrams[2] = decrypt_bigrams_trigrams(candidate_letters_bigrams_trigrams[2])

            if not is_consistent(bigrams=candidate_letters_bigrams_trigrams[1], trigrams=candidate_letters_bigrams_trigrams[2]):
                erase_decrypt_attempt(plain_text=PLAIN_TEXT, index_list=cipher_letter_index_list)
                DECRYPT_KEY[candidate_letter] = '*'
            
            else:
                char_slices = list(filter(('').__ne__, ''.join(PLAIN_TEXT).split('*')))

                consistent_slice = True                

                for slice in char_slices:
                    if not is_consistent(slice):
                        erase_decrypt_attempt(plain_text=PLAIN_TEXT, index_list=cipher_letter_index_list)
                        DECRYPT_KEY[candidate_letter] = '*'
                        consistent_slice = False
                        break

                if consistent_slice:
                    if '*' not in PLAIN_TEXT:  # It means the cipher text was decrypted successfully
                        save_decrypt_attempt()
                        return True

                    if generate_decrypt_key():
                        return True
                    else:
                        erase_decrypt_attempt(plain_text=PLAIN_TEXT, index_list=cipher_letter_index_list)
                        DECRYPT_KEY[candidate_letter] = '*'

    return False


def reset_defaults():
    for i in range(len(PLAIN_TEXT)):
        PLAIN_TEXT[i] = '*'

    for key in DECRYPT_KEY:
        DECRYPT_KEY[key] = '*'


def read_decrypt_attempt():
    attempt = 0

    with open('mono_decrypt_attempt.txt', 'r') as file:
        for line in file:
            splited_line = line.split(": ")

            if splited_line[0] == "Counter":
                attempt = splited_line[1]

    return int(re.sub(r'[^0-9]', '', attempt))


def decrypt_cipher():
    
    global cipher_text_mappings, sociability_average, counter
    
    # Analyzes the given cipher text and returns a list of four dicts, where the first one is the cipher text's letter frequency mapping, the second is the letter sociability mapping, the third one is the bigram mapping and the last one is the trigram mapping
    cipher_text_mappings = analyze_cipher_text(cipher_text=cipher_text)

    sociability_average = sum(cipher_text_mappings[1].values()) / len(cipher_text_mappings[1])

    counter = 0

    reversed_ = dict(reversed(list(cipher_text_mappings[0].items())))

    decrypt_attempt = read_decrypt_attempt()

    for perm in itertools.permutations(reversed_.items()):
        if counter >= decrypt_attempt:
            cipher_text_mappings[0] = dict(reversed(list(dict(perm).items())))
        
            generate_decrypt_key()

            reset_defaults()

        counter += 1

        if counter >= 1000:
            break


with open('Grupo07_texto_cifrado.txt', 'r') as cipher_file:
    cipher = cipher_file.read()

global cipher_text
cipher_text = cipher

plain_text = decrypt_cipher()
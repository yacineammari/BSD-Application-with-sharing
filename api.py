import string
import itertools
from math import sqrt
letter_freq = {
    'a':0.07636,
    'b':0.00901,
    'c':0.0326,
    'd':0.03669,
    'e':0.14715,
    'f':0.01066,
    'g':0.00866,
    'h':0.00737,
    'i':0.07529,
    'j':0.00613,
    'k':0.00074,
    'l':0.05456,
    'm':0.02968,
    'n':0.07095,
    'o':0.05796,
    'p':0.02521,
    'q':0.01362,
    'r':0.06693,
    's':0.07948,
    't':0.07244,
    'u':0.06311,
    'v':0.01838,
    'w':0.00049,
    'x':0.00427,
    'y':0.00128,
    'z':0.00326
}
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
def stander_text(text):
    '''Make text lower case with no spaces and change speacle letter to the 26 accpeted'''
    text = text.lower()
    text = text.replace(' ','')
    text = text.replace('’','')
    text = text.replace(':','')
    text = text.replace('/','')
    text = text.replace('.','')
    text = text.replace(';','')
    changes = {
        'à':'a',
        'â':'a',
        'ç':'c',
        'é':'e',
        'è':'e',
        'ê':'e',
        'î':'i',
        'ô':'o',
        'û':'u',
        'ù':'u',
    }

    for c in changes.keys():
        text = text.replace(c,changes[c])

    return text

def stander_text2(text):
    '''Make text lower case with no spaces and change speacle letter to the 26 accpeted'''
    text = text.replace(' ','')
    text = text.replace('’','')
    text = text.replace(':','')
    text = text.replace('/','')
    text = text.replace('.','')
    text = text.replace(';','')
    changes = {
        'à':'a',
        'â':'a',
        'ç':'c',
        'é':'e',
        'è':'e',
        'ê':'e',
        'î':'i',
        'ô':'o',
        'û':'u',
        'ù':'u',
    }

    for c in changes.keys():
        text = text.replace(c,changes[c])

    return text

def gen_alpha_map():
    '''generate the alphabite map'''
    alpha = list(string.ascii_lowercase)

    map_text_to_number = {}  # text -> int
    map_number_to_text = {}  # int -> text

    for i in range(len(alpha)):
        map_text_to_number[alpha[i]] = i
        map_number_to_text[i] = alpha[i]

    return [map_text_to_number, map_number_to_text]

def encode_caesar(text, n, map_text_to_number, map_number_to_text):
    '''caesar encoding function'''
    c_text = ''
    for t in text:
        try:
            c_text = c_text + map_number_to_text[(map_text_to_number[t]+n) % 26]
        except KeyError:
            pass

    return c_text

def decode_caesar(text, n, map_text_to_number, map_number_to_text):
    '''decoding the caesar cipher'''
    d_text = ''

    for t in text:
        try:
            d_text = d_text + \
                map_number_to_text[(map_text_to_number[t]-n) % 26]
        except KeyError:
            pass

    return d_text

def encode_vigenere(text, key, map_text_to_number, map_number_to_text):
    '''the vigenere cipher encoding fun'''
    c_text = ''
    j = 0
    for t in text:
        if j == len(key):
            j = 0
        try:
            c_text = c_text + \
                map_number_to_text[(map_text_to_number[t] +
                                    map_text_to_number[key[j]]) % 26]
        except KeyError:
            j = j - 1
        j = j + 1

    return c_text

def decode_vigenere(text, key, map_text_to_number, map_number_to_text):
    '''the vigenner chipher decoding'''
    c_text = ''
    j = 0
    for t in text:
        if j == len(key):
            j = 0
        try:
            c_text = c_text + \
                map_number_to_text[(map_text_to_number[t] -
                                    map_text_to_number[key[j]]) % 26]
        except KeyError:
            j = j - 1
        j = j + 1

    return c_text

def encode_substitution(text, alpha_map):
    '''substitution encoding function'''
    c_text = ''

    for t in text:
        try:
            c_text = c_text + alpha_map[t]
        except KeyError:
            pass

    return c_text

def decode_substitution(text, alpha_map_rev):
    '''substitution encoding function'''
    d_text = ''
    for t in text:
        try:
            d_text = d_text + alpha_map_rev[t]
        except KeyError:
            pass

    return d_text

def encode_Transposition(text, n):
    if len(text) % n != 0:
        text = text + ('X' * (n - (len(text) % n)))
    j = 0

    c_text = ''
    for j in range(n):
        i = 0
        while i < len(text):
            c_text = c_text + text[j+i]
            i = i + n

    return c_text

def decode_Transposition(text, n):
    declage = int(len(text) / n)
    j = 0
    c_text = ''
    for j in range(declage):
        i = 0
        while i < len(text):
            c_text = c_text + text[j+i]
            i = i + declage

    return c_text.replace('X', '')

def subtext(n, len_key, text):
    '''cut the text into len_key blocks'''
    i = n 
    letters = []
    while i < len(text):
        letters.append(text[i])
        i += len_key
    return ''.join(letters)

def gen_keys(list_of_letters,DEPTH,key_len):
    list_of_keys = []
    for indexes in itertools.product(range(DEPTH), repeat=key_len):
        possibleKey = ''
        for i in range(key_len):
            possibleKey += list_of_letters[i][indexes[i]]
        list_of_keys.append(possibleKey)

    return list_of_keys

def hack_key(text,len_key):
    '''cracke the vignner cipher'''
    DEPTH = 3
    key = []

    blocs = []
    for i in range(len_key):
        blocs.append(subtext(i,len_key,text))

    for bloc in blocs:
        bloc_len = len(bloc)

        # Count letters.
        c = dict((key, 0) for key in LETTERS)

        for char in bloc:
            c[char] += 1
        
        # Compute letter freq.
        text_letter_freq = dict((key, float(c[key]) / bloc_len) for key in c)
        # all action is here
        letter_freq_tuple = []
        for i in range(26):
            total_freq = 0
            letter_g = chr(i + 97)
            for j in range(26):
                pi = letter_freq[chr(j + 97)]
                hig = text_letter_freq[chr(((i + j) % 26) + 97)]
                total_freq +=  pi*hig  

            letter_freq_tuple.append((letter_g, total_freq))
        letter_freq_tuple.sort(key=lambda tup: tup[1], reverse=True)
        pssible__letter_list = []
        for elem in letter_freq_tuple[:DEPTH]:
            pssible__letter_list.append(elem[0])
        key.append(pssible__letter_list)
    
    return gen_keys(key,DEPTH,len_key)

def get_freq(text):
    c = dict((key, 0) for key in LETTERS)
    for char in text:
        c[char] += 1    
    return list(c.values())

def fluctu(p,n):
    e = 1.96 * sqrt(p * (1 - p) / n)
    return [p - e, p + e]
 
def interfluctu(l1,l2):
    s1 = sum(l1) # text freq
    s2 = sum(l2) # franche freq
    ok = 0
    for i in range(26):
        bornes = fluctu(l2[i]/s2,s1)

        if bornes[0] <= l1[i]/s1 <= bornes[1]:
            ok += 1
    return int(100 * ok / 26) 

def france_percentage(text):
    l1 = get_freq(text)
    l2 = [763,90,326,366,1471,106,86,73,752,54,4,545,296,709,537,302,136,655,794,724,631,162,11,38,30,13]
    return interfluctu(l1,l2)



def hack_viginner(text,len_key,map_text_to_number,map_number_to_text):
    list_of_keys = hack_key(text,len_key)
    res = []
    for key in list_of_keys:
        dtext = decode_vigenere(text,key,map_text_to_number,map_number_to_text)
        res.append(['key: '+str(key),france_percentage(dtext),dtext])
    res.sort(key=lambda l: l[1], reverse=True)
    return res
    

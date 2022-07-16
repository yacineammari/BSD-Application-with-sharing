
def xor(bloc1,bloc2):
    '''XOR'''
    x = ''
    for i in range(len(bloc1)):
        if bloc1[i] == bloc2[i]:
            x = x + '0'
        else:
            x = x + '1'

    return x 

def permutation(text,tab):
    '''permutation'''
    return ''.join(list(map(lambda x: text[x], tab)))

def split_to_gd(text):
    g = text[0:int(len(text)/2)]
    d = text[int(len(text)/2):]
    return [g,d]

def bloc_to_binary(bloc):
    '''code every chr on 8 bit from it asscii code'''
    return ''.join(format(ord(i),'b').zfill(8) for i in bloc)

def initial_permutation(bloc):
    '''initial_permutation of DES'''
    ip = [57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]
    return permutation(bloc,ip)  

def f_funtion(bloc,key):
    return perm_f(s_boxs(xor(e(bloc),key)))

def e(bloc):
    '''take a text of 32bits and make it a 48bits'''
    expansion_table = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

    return permutation(bloc,expansion_table) 

def s_box(indece,bloc):
    '''s box'''
    sbox = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

    tab_num = indece - 1
    row = int(bloc[0] + bloc[5],2)
    colum = int(bloc[1:5],2)
    elem = (16 * row) + colum	
    return bin(sbox[tab_num][elem])[2:].zfill(4)

def s_boxs(text):
	text = str(text)	
	sbox1 = str(s_box(1,text[0:6]))
	sbox2 = str(s_box(2,text[6:12]))
	sbox3 = str(s_box(3,text[12:18]))
	sbox4 = str(s_box(4,text[18:24]))
	sbox5 = str(s_box(5,text[24:30]))
	sbox6 = str(s_box(6,text [30:36]))
	sbox7 = str(s_box(7,text[36:42]))
	sbox8 = str(s_box(8,text [42:48]))  
	return sbox1+sbox2+sbox3+sbox4+sbox5+sbox6+sbox7+sbox8

def perm_f(bloc):
    '''function permutation'''
    p = [
        15, 6, 19, 20, 28, 11,
        27, 16, 0, 14, 22, 25,
        4, 17, 30, 9, 1, 7,
        23,13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10,
        3, 24
    ]

    return permutation(bloc,p)

def pc1(key):
    pc1 = [56, 48, 40, 32, 24, 16,  8,
    0, 57, 49, 41, 33, 25, 17,
    9,  1, 58, 50, 42, 34, 26,
    18, 10,  2, 59, 51, 43, 35,
    62, 54, 46, 38, 30, 22, 14,
    6, 61, 53, 45, 37, 29, 21,
    13,  5, 60, 52, 44, 36, 28,
    20, 12,  4, 27, 19, 11,  3 ]

    return permutation(key,pc1)

def pc2(key):
    pc2 = [
		13, 16, 10, 23,  0,  4,
		2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

    return permutation(key,pc2) 

def lsi(bloc,i):
    left_rotations = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    if left_rotations[i] == 1:
        return bloc[1::]+bloc[0]
    else:
        return bloc[2::]+bloc[0:2]

def gen_keys(seed):
    key_56bit = pc1(seed)
    list_of_keys = [] 
    g ,d = split_to_gd(key_56bit)

    for i in range(16):
        g = lsi(g,i)
        d = lsi(d,i)
        list_of_keys.append(pc2(g+d))
    return list_of_keys

def final_permutation(text):
    fp = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]

    return permutation(text,fp)

def b_bloc_str(fp):
	t = ''
	for i in range(0,len(fp),8): 
		t = t + chr(int(fp[i:i+8],2))
	
	return t

def encode(text,lkeys,binnary=True):
	text = initial_permutation(text)

	L,R = split_to_gd(text)

	for key in lkeys:
		Ln = R
		Rn = xor(L,f_funtion(R,key)).zfill(32)

		L = Ln
		R = Rn
	
	fp = final_permutation(R+L)
	if binnary:
		return fp
	else:
		return b_bloc_str(fp)



def decode(text,lkeys):
	text = initial_permutation(text)

	L,R = split_to_gd(text)

	for key in lkeys:
		Ln = R
		Rn = xor(L,f_funtion(R,key)).zfill(32)

		L = Ln
		R = Rn
	fp = final_permutation(R+L)
	 
	return b_bloc_str(fp)


def des_encode(text,seed,binnary=True):
	#creating the keys from the seed
	lkey = gen_keys(bloc_to_binary(seed))

	ctext = ''

	#calibrating the text 
	if len(text) % 8 !=0:
		text = text + (' '*(8 - len(text) % 8))

	#cutting the text into 64bits text 
	
	list_of_bloc = []
	
	for i in range(0,len(text),8):
		list_of_bloc.append(bloc_to_binary(text[i:i+8]))
	
	for bloc in list_of_bloc:
		ctext = ctext + encode(bloc,lkey,binnary)
	
	return ctext



def des_decode(text,seed):
	#creating the keys from the seed
	lkey = gen_keys(bloc_to_binary(seed))

	dtext = ''

	#cutting the text into 64bits text
	list_of_bloc = []
	
	for i in range(0,len(text),64):
		list_of_bloc.append(text[i:i+64])

	for bloc in list_of_bloc:
		dtext = dtext + decode(bloc,lkey[::-1])
	
	padded_text = dtext[-8:].strip()
	# padded_text = padded_text.replace('*******','') #7
	# padded_text = padded_text.replace('******','') #6
	# padded_text = padded_text.replace('*****','') #5
	# padded_text = padded_text.replace('****','') #4
	# padded_text = padded_text.replace('***','') #3
	# padded_text = padded_text.replace('**','') #2	
	return dtext[0:-8] + padded_text








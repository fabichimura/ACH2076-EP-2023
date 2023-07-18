import numpy as np
import itertools

#https://www.palavras.net
digramas_filtro = ['aa', 'ah','ak', 'aw', 'ay', 
                   'bb', 'bc', 'bd', 'bf', 'bg', 'bh', 'bk', 'bm', 'bn','bp', 'bq', 'bw', 'bx', 'by', 'bz', 
                   'cb', 'cc', 'cd', 'cf', 'cg', 'cj', 'ck', 'cm', 'cn','cp', 'cq', 'cs', 'cv', 'cw', 'cx', 'cy', 'cz',
                   'db', 'dc', 'dd', 'df', 'dg', 'dh', 'dj', 'dk', 'dl', 'dn', 'dp', 'dq', 'dt', 'dw', 'dx', 'dy', 'dz',
                   'ee', 'eh', 'ek','ew', 'ey',
                   'fb', 'fc', 'fd', 'ff', 'fg', 'fh', 'fj', 'fk', 'fm', 'fn', 'fp', 'fq', 'ft','fs', 'fv', 'fw', 'fx', 'fy', 'fz',
                   'gb', 'gc', 'gd', 'gg', 'gh', 'gj', 'gk', 'gp', 'gq', 'gs', 'gt', 'gv', 'gw', 'gy', 'gx', 'gz',
                   'hv', 'hc', 'hf', 'hg', 'hh', 'hj', 'hk','hl', 'hm', 'hn', 'hp', 'hq', 'hr', 'hs', 'ht', 'hv', 'hw', 'hx', 'hy', 'hz',
                   'ih', 'ii', 'ik', 'iw', 'iy',
                   'jb', 'jc', 'jd', 'jf', 'jg', 'jh', 'jj', 'jk', 'jl', 'jm', 'jn', 'jp', 'jq', 'jr', 'js', 'jt', 'jv', 'jw', 'jx', 'jy', 'jz',
                   'kb', 'kc', 'kd', 'kf', 'kg', 'kj', 'kk', 'kl', 'km', 'kn', 'kp', 'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz',
                   'lj', 'lk', 'lw', 'll', 'ln', 'lq', 'lw','lx', 'ly', 'lz', 
                   'mc','md', 'mf', 'mg', 'mh', 'mj', 'mk',  'ml', 'mm', 'mn','mq', 'mr', 'ms', 'mt', 'mv', 'mw', 'my', 'mx', 'mz',
                   'nb', 'nk', 'nn', 'nm', 'np', 'nw', 'ny', 
                   'oh', 'ok', 'oo',  'ow', 'oy',
                   'pb', 'pd', 'pf', 'pg', 'ph', 'pj', 'pk', 'pm', 'pn', 'pp','pq', 'pv', 'pw', 'px', 'py' ,'pz',
                   'qa', 'qb', 'qc', 'qd', 'qe', 'qf','qg' , 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt', 'qv', 'qw', 'qx', 'qy', 'qz',
                   'rh', 'rk', 'rw', 'ry', 'rx',
                   'sh', 'sj', 'sk', 'sw', 'sx', 'sy', 'sz',
                   'tb', 'tc','td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'tq', 'ts', 'tv', 'tt','tw', 'tx', 'ty', 'tz', 
                   'uh', 'uk', 'uu', 'uw', 'uy',
                   'vb', 'vc', 'vd', 'vf', 'vg', 'vh', 'vj', 'vk', 'vl', 'vm', 'vn', 'vp', 'vq', 'vs', 'vv','vt', 'vw', 'vx','vy', 'vz',
                   'wb', 'wc', 'wd', 'wf', 'wg', 'wh', 'wj', 'wk' , 'wl', 'wm', 'wn', 'wp', 'wq', 'wr', 'ws', 'wt', 'wv','ww', 'wx', 'wy','wz',
                   'xb', 'xc', 'xd', 'xf', 'xg', 'xh', 'xj', 'xk', 'xl', 'xm', 'xn', 'xp', 'xq','xr','xs','xt', 'xw', 'xy','xx', 'xz',
                   'yb', 'yc', 'yd', 'yf', 'yg', 'yh', 'yj', 'yk', 'yl', 'ym', 'yn', 'yp', 'yq','yr', 'ys', 'yt', 'yv', 'yw', 'yx', 'yy', 'yz',
                   'zb', 'zc', 'zd', 'zf', 'zg', 'zh', 'zj', 'zk', 'zl', 'zm', 'zn', 'zp', 'zq', 'zr', 'zs', 'zt', 'zv', 'zw', 'zx', 'zy', 'zz' ]    

trigramas_filtro = [ 
                    'aea', 'aeb', 'aef', 'aeg', 'aeh','aei','aej', 'aem', 'aeo', 'aep', 'aeq', 'aeu', 'aev', 'aez'
                    'aif', 'aig', 'aih', 'aij', 'aiq',
                    'aoa', 'aob', 'aoc', 'aod', 'aoe', 'aof', 'aog', 'aoh', 'aoi', 'aoj', 'aol', 'aom', 'aon', 'aop', 'aoq', 'aos','aot', 'aou', 'aov','aoz',
                    'aua', 'aub', 'auf', 'auh', 'aui', 'auj', 'auo', 'aup', 'auu', 'auv' , 'auz',
                    'eae', 'eaf','eah', 'eai', 'eao', 'eaq', 'ear', 'eau', 'eav', 'eaz',
                    'eia', 'eib', 'eie', 'eih', 'eil', 'eim', 'ein', 'eip','eiq','eis', 'eiu','eiv', 'eiz',
                    'eoa', 'eob','eoh','eoi','eoj', 'eoq','eou','eojv','eoz',
                    'eua', 'eub', 'euc', 'eue', 'euh', 'eui', 'euj', 'eul', 'euo', 'euq', 'euv', 'euz',
                    'iae', 'iah','iai','iaj','iao','iaq', 'iau','iav',
                    'iea', 'ieb', 'iec','ief','ieg','ieh','iej','iem', 'ieo', 'iep', 'ieq', 'ieu', 'iev', 'iez',
                    'ioe', 'ioh','ioi', 'ioj','ioo','ioq','iou', 'iov', 'ioz'
                    'iua', 'iub', 'iuc', 'iud', 'iue', 'iuf', 'iug', 'iuh', 'iui', 'iuj', 'iul' , 'iuo', 'iup', 'iuq', 'ius', 'iut' , 'iuu', 'iuv', 'iuz',
                    'oab', 'oae', 'oaf', 'oah', 'oai','oaj','oam','oao','oap','oaq','oat','oau','oav','oaz',
                    'oea', 'oeb', 'oee', 'oef', 'oeg', 'oeh', 'oej', 'oel', 'oeo', 'oep', 'oeq','oea', 'oeu','oev','oez',
                    'oib', 'oie','oif', 'oig', 'oih', 'oij', 'oip','oiq','oiu','oiv', 'oiz',
                    'oua', 'oub', 'oud','oue','ouf', 'oug','ouh','oui', 'ouj', 'oum','oun','ouq', 'ouu', 'ouz',
                    'uae', 'uaf','uag','uah','uao', 'uaq','uau', 'uav','uaz',
                    'ued','uee','uef','ueg', 'ueh','uep','ueu', 'uev','uez',
                    'uib','uif','uig','uih','uij','uiq','uiu',
                    'uoa', 'uob', 'uoe', 'uof',  'uog', 'uoh', 'uoi', 'uoj', 'uol', 'uom', 'uon',  'uoo',  'uop', 'uoq', 'uot', 'uou', 'uov',  'uoz',     
                    ]

def salvar_dados_arquivo(dados):
    try:
        arquivo = open("dados.txt", "a")
        for dado in dados:
            arquivo.write(dado)
        arquivo.write('\n')
        arquivo.close()
        print("Dados salvos com sucesso!")
    except Exception as e:
        print("Ocorreu um erro ao salvar os dados:", str(e))

def substituir_por_posicao(frase):
    lista_numeros = []
    for letra in frase:
        posicao = ord(letra.lower()) - ord('a')
        lista_numeros.append(posicao)
    return lista_numeros

def substituir_por_letra(numero):
    if 0 <= numero <= 25:
        letra = chr(numero + ord('a'))
        return letra
    else:
        return ""
    
def calcula_mod_26(num):
    if(num > 0):
        return num % 26
    elif(num < 0):
        while num < 0:
            num += 26
        return num
    else:
        return 0
    
def diferenca_posicao_mod26(texto1, texto2):
    diferenca_posicoes_mod26 = []
    for i in range(len(texto1)):
        diferenca_posicoes_mod26.append(calcula_mod_26(texto1[i] - texto2[i]))
    return diferenca_posicoes_mod26

#As vogais A, E, I, O, U e as consoantes S, R, N, D, M formam mais de 3/4 dos textos em Português. - https://www.gta.ufrj.br/grad/06_2/alexandre/criptoanalise.html
def verifica_porcentagem_letras_comuns(texto):
    total_caracteres = len(texto)
    total_a = texto.count('a')
    total_e = texto.count('e')
    total_i = texto.count('i')
    total_o = texto.count('o')
    total_u = texto.count('u')
    total_s = texto.count('s')
    total_r = texto.count('r')
    total_n = texto.count('n')
    total_d = texto.count('d')
    total_m = texto.count('m')

    porcentagem_a = (total_a / total_caracteres) * 100
    porcentagem_e = (total_e / total_caracteres) * 100
    porcentagem_i = (total_i / total_caracteres) * 100
    porcentagem_o = (total_o / total_caracteres) * 100
    porcentagem_u = (total_u / total_caracteres) * 100
    porcentagem_s = (total_s / total_caracteres) * 100
    porcentagem_r = (total_r / total_caracteres) * 100
    porcentagem_n = (total_n / total_caracteres) * 100
    porcentagem_d = (total_d / total_caracteres) * 100
    porcentagem_m = (total_m / total_caracteres) * 100

    porcentagem_total = porcentagem_a + porcentagem_e + porcentagem_i + porcentagem_o + porcentagem_u \
        + porcentagem_s + porcentagem_r + porcentagem_n + porcentagem_d + porcentagem_m 

    if porcentagem_total >= 50:
        return True
    else:
        return False


with open('EP_Seguranca_informacao\Texto_desconhecido\Cifrado\Vigenere\Grupo07_texto_cifrado1.txt','r') as arquivo:
    texto_cifrado_1 = arquivo.read()

with open('EP_Seguranca_informacao\Texto_desconhecido\Cifrado\Vigenere\Grupo07_texto_cifrado2.txt','r') as arquivo:
    texto_cifrado_2 = arquivo.read()


lista_permutacoes = list(itertools.product([0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21], repeat=6))

print(len(lista_permutacoes))

posicoes_cifrado_1 = substituir_por_posicao(texto_cifrado_1)
posicoes_cifrado_2 = substituir_por_posicao(texto_cifrado_2)
print(posicoes_cifrado_1)
print(posicoes_cifrado_2)

diferenca_posicoes_texto_encriptados = diferenca_posicao_mod26(posicoes_cifrado_1, posicoes_cifrado_2)
print('Esta e a diferenca das posicoes dos textos(mod26):',diferenca_posicoes_texto_encriptados)

for permutacao in lista_permutacoes:
    posicoes_res1 = []
    posicoes_res2 = []
    texto_1 = ''
    texto_2 = ''
    diferenca_posicoes_iguais = False
    filtro_digrama = False
    filtro_trigrama = False
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[0] - permutacao[0]))
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[1] - permutacao[1]))
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[2] - permutacao[2]))
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[3] - permutacao[3]))
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[4] - permutacao[4]))
    posicoes_res1.append(calcula_mod_26(posicoes_cifrado_1[5] - permutacao[5]))

    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[0] - permutacao[0])) 
    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[1] - permutacao[1]))
    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[2] - permutacao[2]))
    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[3] - permutacao[3]))
    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[4] - permutacao[4]))
    posicoes_res2.append(calcula_mod_26(posicoes_cifrado_2[5] - permutacao[5]))

    diferenca_posicoes_permutacoes = diferenca_posicao_mod26(posicoes_res1, posicoes_res2)
    if(diferenca_posicoes_permutacoes == diferenca_posicoes_texto_encriptados):
        diferenca_posicoes_iguais = True

    texto_1 = substituir_por_letra(posicoes_res1[0]) + substituir_por_letra(posicoes_res1[1])\
        + substituir_por_letra(posicoes_res1[2]) + substituir_por_letra(posicoes_res1[3])\
        + substituir_por_letra(posicoes_res1[4]) + + substituir_por_letra(posicoes_res1[5])
    texto_2 = substituir_por_letra(posicoes_res2[0]) + substituir_por_letra(posicoes_res2[1])\
        + substituir_por_letra(posicoes_res2[2]) + substituir_por_letra(posicoes_res2[3]) \
        + substituir_por_letra(posicoes_res2[4]) + substituir_por_letra(posicoes_res2[5])

    if  (texto_1[0] +  texto_1[1]) not in digramas_filtro\
    and (texto_1[1] +  texto_1[2]) not in digramas_filtro\
    and (texto_1[2] +  texto_1[3]) not in digramas_filtro\
    and (texto_1[3] +  texto_1[4]) not in digramas_filtro\
    and (texto_1[4] +  texto_1[5]) not in digramas_filtro\
    and (texto_2[0] +  texto_2[1]) not in digramas_filtro\
    and (texto_2[1] +  texto_2[2]) not in digramas_filtro\
    and (texto_2[2] +  texto_2[3]) not in digramas_filtro\
    and (texto_2[3] +  texto_2[4]) not in digramas_filtro\
    and (texto_2[4] +  texto_2[5]) not in digramas_filtro:
        filtro_digrama = True

    if  (texto_1[0] +  texto_1[1] + texto_1[2] ) not in trigramas_filtro\
    and  (texto_1[1] +  texto_1[2] + texto_1[3] ) not in trigramas_filtro\
    and  (texto_1[2] +  texto_1[3] + texto_1[4] ) not in trigramas_filtro\
    and  (texto_1[3] +  texto_1[4] + texto_1[5] ) not in trigramas_filtro\
    and  (texto_2[0] +  texto_2[1] + texto_2[2] ) not in trigramas_filtro\
    and  (texto_2[1] +  texto_2[2] + texto_2[3] ) not in trigramas_filtro\
    and  (texto_2[2] +  texto_2[3] + texto_2[4] ) not in trigramas_filtro\
    and  (texto_2[3] +  texto_2[4] + texto_2[5] ) not in trigramas_filtro:
        filtro_trigrama = True

    if (filtro_digrama and filtro_trigrama and diferenca_posicoes_iguais and (verifica_porcentagem_letras_comuns(texto_1) and verifica_porcentagem_letras_comuns(texto_2))\
        and('k' not in texto_1) and ('k' not in texto_2) and ('w' not in texto_1 ) and ('w' not in texto_2) and ('x' not in texto_1) and ('x' not in texto_2)\
        and ('y' not in texto_1) and ('y' not in texto_2) and('z' not in texto_1) and('z' not in texto_2)):
        print('==================================')
        print(diferenca_posicoes_permutacoes)
        print(permutacao)
        print(posicoes_res1)
        print(texto_1)
        print(posicoes_res2)
        print(texto_2)
        salvar_dados_arquivo('-------------------------')
        salvar_dados_arquivo(str(permutacao))
        salvar_dados_arquivo(texto_1)
        salvar_dados_arquivo(texto_2)
        salvar_dados_arquivo('-------------------------')
        print('==================================')



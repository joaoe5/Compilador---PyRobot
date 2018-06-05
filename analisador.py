# -*- coding: utf-8 -*-
import ply.lex as lex
import re

reserved = {
	'begin': 'INI_CODE',
	'end': 'FIM_CODE',
	'start': 'LIGA_ROBO',
	'off': 'DESLIGA_ROBO',
	'stop': 'PARAR',
	'if': 'IF',
	'else': 'ELSE',
	'loop': 'WHILE',
	'break': 'BREAK',
	'print': 'EXIBA',
}

tokens = [
	'COMENTARIO',
	'OP_RELACIONAL', 'OP_ARITMETICO',
	'A_PARENTE', 'F_PARENTE',
	'A_CHAVES', 'F_CHAVES',
	'QUEBRA_LINHA',
	'TIPO_BOOL',
	'TIPO_VAR',
	'STRING',
	'NUMERO',
	'ATRIBUIR',
	'VARIAVEL',
	'DIR_ROBO',
	'MOVE_ROBO',
] + list(reserved.values())

t_STRING = r'\["[^\"\]]*"\]'
t_COMENTARIO = r"[\/][\*]+[\w\W]+[\*]+[\/]"
t_A_PARENTE = r"\("
t_F_PARENTE = r"\)"
t_OP_RELACIONAL = r"((<=){1})|((>=){1})|((==){1})|((!=){1})|((<){1})|((>){1})"
t_OP_ARITMETICO = r"[\+|\-|\/|\*]"
t_ATRIBUIR = r"="
t_A_CHAVES = r"[\{]"
t_F_CHAVES = r"[\}]"
t_QUEBRA_LINHA = r";+"
t_TIPO_BOOL = r"(false)|(true)"
t_TIPO_VAR = r"(int)|(float)|(bool)|(str)"
t_NUMERO = r"[\d]+"
t_VARIAVEL = r"(var_)[\d]+"
t_DIR_ROBO = r"(right)|(left)"
t_MOVE_ROBO = r"(forward)|(backward)"

def t_RESERVED(t):
	r"(begin)|(end)|(start)|(off)|(right)|(left)|(stop)|(if)|(else)|(loop)|(break)|(print)"
	t.type = reserved.get(t.value, 'RESERVED')
	return t

# Regra para quebra de linhas(rastrear)
def t_newline(t):
	# t.lexer.lineno = 0
	r'\n+'
	t.lexer.lineno += len(t.value)

# Uma string contendo caracteres ignorados (espaços e tabulações)
t_ignore = ' \t\r'

# Erro ao manipular regra
def t_error(t):
	erro = ''
	erro = "Illegal character '{0}' na linha {1} coluna {2}".format(t.value[0], t.lineno, t.lexpos)
	print(erro)
	#lista.append(erro)
	t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

# precedence = (
# 	('left', 'begin'),
# 	('right', 'end')
# )

names = {}
#NOVA GRAMATICA

def p_programa(t):
    '''programa : INI_CODE A_CHAVES listacorpo F_CHAVES FIM_CODE
				| INI_CODE A_CHAVES empty F_CHAVES FIM_CODE
				| comentario
	'''

def p_corpo(t):
    '''corpo : declaracao 
            | atribuicao
            | loop
            | direcao
            | movimenta
            | iniciarobo
            | break
            | condicional 
            | parar
			| mostrar
			| comentario
    '''

def p_corpo_robo_on(t):
    '''corpo_robo_on : declaracao
            | atribuicao
            | loop_robo_on
            | direcao
            | movimenta
            | break
            | condicional_robo_on
            | parar
			| mostrar
			| comentario
    '''

def p_empty(t):
	'empty : '
	pass

def p_listacorpo(t):
    '''listacorpo : corpo
                | corpo listacorpo
    '''

def p_listacorpo_robo_on(t):
    '''listacorpo_robo_on : corpo_robo_on
                | corpo_robo_on listacorpo_robo_on
    '''

def p_declaracao(t):
    'declaracao : TIPO_VAR VARIAVEL QUEBRA_LINHA'

def p_atribuicao(t):
    '''atribuicao : VARIAVEL ATRIBUIR operacao QUEBRA_LINHA
				| VARIAVEL ATRIBUIR expressao_str QUEBRA_LINHA
				| VARIAVEL ATRIBUIR expressao QUEBRA_LINHA
				| VARIAVEL ATRIBUIR booleano QUEBRA_LINHA
	'''

def p_operacao(t):
    '''operacao : expressao OP_ARITMETICO expressao
				| expressao OP_ARITMETICO operacao
	'''

def p_expressao_num(t):
    'expressao : NUMERO'

def p_expressao_var(t):
    'expressao : VARIAVEL'

def p_expressao_string(t):
    'expressao_str : STRING'

def p_expressao_boolean(t):
    'booleano : TIPO_BOOL'

def p_loop(t):
    '''loop : WHILE A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo F_CHAVES
            | WHILE A_PARENTE TIPO_BOOL F_PARENTE A_CHAVES listacorpo F_CHAVES
			| WHILE A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES
            | WHILE A_PARENTE TIPO_BOOL F_PARENTE A_CHAVES empty F_CHAVES
    '''

def p_loop_robo_on(t):
    '''loop_robo_on : WHILE A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo_robo_on F_CHAVES
            		| WHILE A_PARENTE TIPO_BOOL F_PARENTE A_CHAVES listacorpo_robo_on F_CHAVES
					| WHILE A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES
            		| WHILE A_PARENTE TIPO_BOOL F_PARENTE A_CHAVES empty F_CHAVES
    '''

def p_comparacao(t):
    '''comparacao : VARIAVEL OP_RELACIONAL NUMERO
                | VARIAVEL OP_RELACIONAL VARIAVEL
    '''

def p_condicional(t):
    '''condicional : IF A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo F_CHAVES
                | IF A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo F_CHAVES ELSE A_CHAVES listacorpo F_CHAVES
				| IF A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES
                | IF A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES ELSE A_CHAVES empty F_CHAVES
	'''

def p_condicional_robo_on(t):
    '''condicional_robo_on : IF A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo_robo_on F_CHAVES
                		| IF A_PARENTE comparacao F_PARENTE A_CHAVES listacorpo_robo_on F_CHAVES ELSE A_CHAVES listacorpo_robo_on F_CHAVES
						| IF A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES
                		| IF A_PARENTE comparacao F_PARENTE A_CHAVES empty F_CHAVES ELSE A_CHAVES empty F_CHAVES
	'''

def p_iniciarobo(t):
    '''iniciarobo : LIGA_ROBO QUEBRA_LINHA listacorpo_robo_on DESLIGA_ROBO QUEBRA_LINHA
				| LIGA_ROBO QUEBRA_LINHA empty DESLIGA_ROBO QUEBRA_LINHA
	'''

def p_break(t):
    'break : BREAK QUEBRA_LINHA'

def p_direcao(t):
    'direcao : DIR_ROBO QUEBRA_LINHA'

def p_parar(t):
    'parar : PARAR QUEBRA_LINHA'

def p_movimenta(t):
	'movimenta : MOVE_ROBO QUEBRA_LINHA'

def p_mostrar(t):
	'''mostrar : EXIBA STRING QUEBRA_LINHA
				| EXIBA VARIAVEL QUEBRA_LINHA
				| EXIBA NUMERO QUEBRA_LINHA
	'''

def p_comentario(t):
	'comentario : COMENTARIO'

def p_error(t):
	print("Erro sintatico: " + str(t))

import ply.yacc as yacc
parser = yacc.yacc()

s = '''
begin{
	int var_0;
	var_0 = 12 + var_1 - 10;
	var_1 = ["aaaaa"];
	start;
	print ["TESTE"];
	print 2;
	print var_0;
	loop(true){
		forward;
		if(var_0 == var_1){
			stop;
			break;
		}
		var_1 = var_1 + 1;
	}
	off;
}end
'''

s = '''
begin{
	start;
	loop(true){
		if(var_0 >= 6){
			if(var_1 == 2){
				break;
			}
			else{
				stop;
				forward;
			}
		}
	}
	off;
}end
'''

#Entrada com erro sintático
s1 = '''
begin
	int var_0;
	var_0 = 12 + var_1;
	start;
	loop(true){
		forward;
		if(var_0 == var_1){
			stop;
			break;
		}
		var_1 = var_1 + 1;
	}
	off;
}end
'''

if not s:
	print("Erro ao receber dados")
else:
	parser.parse(s)
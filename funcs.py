#coding:utf8

import re

# 输入一个dict，通过库中每行token
# dict[token] = list中的位置
def trainDict(tokens,token_dict={},vector_length = 0):
	for token in tokens:
		if token not in token_dict.keys():
			token_dict[token] = vector_length
			vector_length+=1
	
	return token_dict,vector_length

# 以各个间隔符分割一行代码，返回一个包含间隔符的token的list
# 字符串和普通变量名应该各自用一个token表示，比如STRING，VAR
def splitCode(code):
	split_list = ['.','\'','"',' ','[',']','(',')','{','}',':','=',',']
	pat_string = '\'(.*?)\'|"(.*?)"|\'\'\'(.*?)\'\'\'' 
	pat_var = '.*?='
	pat_num = '[0-9]+?'
	
	tokens = []
	
	# 将字符串替换为 "STRING"，将变量替换为 SERA_VAR=
	code = re.compile(pat_string).sub('"SERA_STRING"',code) 
	code = re.compile(pat_var).sub('SERA_VAR=',code)
	code = re.compile(pat_num).sub('SERA_NUM',code)
	
	word = ''
	for i in code:
		if i in split_list:
			if word != '':
				tokens.append(word)
				word = ''
			if i != ' ':
				tokens.append(i)
		else:
			word+=i
	return tokens
			
# 输入两个向量(list)，应用余弦定理求出其余弦值
# 公式: cos值 = <vectorA,vectorB> / ( |vectorA|*|vectorB| )
# 即: cos值 = ( x1y1+x2y2+...+xNyN ) / sqrt(x1*x1+x2*x2+...+xN*xN) * sqrt(y1*y1+y2*y2+...+yN*yN)
def getCosine(vectorA,vectorB):
	value1 = 0
	sumA = 0
	sumB = 0
	
	for i in range(len(vectorA)):
		value1+=(vectorA[i]*vectorB[i])
		sumA+=pow(vectorA[i],2)
		sumB+=pow(vectorB[i],2)
	
	value2 = pow(sumA,0.5) * pow(sumB,0.5)
	return value1 / value2
	
# 从目标测试文件中读取每行代码，返回一个list（string）
def getCodes(file_path):
	try:
		pat = '"snippet": "(.*?)"'
		with open(file_path,'r') as file:
			text = file.read()
		r = re.compile(pat).findall(text)
	except Exception as e:
		raise e
	return r
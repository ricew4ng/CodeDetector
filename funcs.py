#coding:utf8

import numpy
import re

# 字符串和普通变量名应该各自用一个token表示，比如STRING，VAR
def replaceCode(code):
	# 先把变量名，字符串，数字替换成 ROVAR,ROSTRING,RONUM
	pat_string = '\'(.+?)\'|"(.+?)"|\'\'\'(.+?)\'\'\'' 
	pat_num = '[0-9]+?'
	pat_var1 = '[a-zA-Z_]+? *='
	pat_var2 = '[a-zA-Z_]+? *,'
	pat_var3 = '[a-zA-Z_]+? *\)'

	code = re.compile(pat_string).sub('"ROSTRING"',code)
	code = re.compile(pat_num).sub('RONUM',code)
	code = re.compile(pat_var1).sub('ROVAR=',code)
	code = re.compile(pat_var2).sub('ROVAR,',code)
	code = re.compile(pat_var3).sub('ROVAR)',code)
	
	return code
	
# 分割库中代码用，以各个间隔符分割一行代码，返回一个包含间隔符的token的list
def code2tokens(code):
	tokens = []
	
	split_list = ['.','\'','"',' ','[',']','(',')','{','}',':','=',',','+','-','>','<']
	word = ''
	for i in code:
		if i not in split_list:
			word+=i
		else:
			if word != '':
				tokens.append(word)
				word = ''
			if i != ' ':
				tokens.append(i)
			
	return tokens
			
# 从目标测试文件中读取每行代码，返回一个list（string）
def getCodes(file_path,isJson=True):
	try:
		if isJson:
			pat = '"snippet": "(.*?)",'
			with open(file_path,'r') as file:
				text = file.read()
			codes = re.compile(pat).findall(text)
		else:
			# codes = []
			# with open(file_path,'r') as file:
				# for line in file:
					
					# codes.append()
			pass
	except Exception as e:
		raise e
	return codes
#coding:utf8

import re

# 字符串和普通变量名应该各自用一个token表示，比如STRING，VAR
def replaceCode(code):
	# 先把变量名，字符串，数字替换成 ROVAR,ROSTRING,RONUM
	pat_string = '\'(.+?)\'|"(.+?)"|\'\'\'(.+?)\'\'\'' 
	pat_num = '[0-9]+'
	pat_var1 = '[a-zA-Z_]+? *='
	pat_var2 = '[a-zA-Z_]+? *,'
	pat_var3 = '[a-zA-Z_]+? *\)'
	code = re.compile(pat_string).sub('"ROSTRING"',code)
	code = re.compile(pat_num).sub('RONUM',code)
	code = re.compile(pat_var1).sub('ROVAR=',code)
	code = re.compile(pat_var2).sub('ROVAR,',code)
	code = re.compile(pat_var3).sub('ROVAR)',code)
	return code
			
# 通过tokens，对dict进行更新,weight是（用行次数表示）权重值，用高优先级token匹配则权重应大一点
def generateDict(tokens=[],text='',dict={},weight=1):
	for token in tokens:
		# r 是list，其中,r[x][0] 是序号+对应行代码；r[x][1]是行序号
		try:
			pat = '(([0-9]+?) .*?'+token+'.*?\n)'
			r = re.compile(pat).findall(text)
		except:
			pat = '(([0-9]+?) .*?\\'+token+'.*?\n)'
			r = re.compile(pat).findall(text)
		for k in r:
			if k[1] in dict.keys():
				dict[k[1]][1]+=weight
			else:
				# 初始化dict的键为某行数的值，为一个list，list[0]是爬到的文本,list[1]是行出现次数
				dict[k[1]] = [k[0],1] 
	return dict
	
# 暂时通过文件读取（后面改成数据库
def getTextByNum(tokens,num_list):
	pass
	
# 输入tokens列表，返回按照优先级划分的2个list
def splitTokensByPRI(tokens):
	h_PRI = ['.','(','['] # 这些字符前的词权重应该是最高的
	low_list = ['.','\'','"',' ','[',']','(',')','{','}',':','=',',','+','-','>','<','RONUM','ROSTRING','ROVAR','%']
	alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	
	h_tokens = [] # 高优先级 tokens
	l_tokens = [] # 低优先级 tokens
	
	for i,token in enumerate(tokens):
		# 如果当前token是 .([中的一个，则前一个token优先级很高
		if token in h_PRI and i != 0: 
			if tokens[i-1] not in low_list and tokens[i-1] not in alpha_list:
				h_tokens.append(tokens[i-1])
		else:
			l_tokens.append(token)
	
	return h_tokens,l_tokens
	
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
			
# 输入codes，（原始无序号，每行为一行代码）
# 输出一份对应的带行号，且每行都是高优先级token 的文本
def generateTokensByPRI(codes,fileName='data/high_tokens_id'):
	with open(fileName,'w') as file:
		for i,code in enumerate(codes):
			code = replaceCode(code)
			tokens = code2tokens(code)
			h_tokens,l_tokens = splitTokensByPRI(tokens)
			
			file.write( str(i)+' '+' '.join(h_tokens)+'\n' )
			
# 从目标测试文件中读取每行代码，返回一个list（string）
def getCodes(file_path,isJson=False):
	try:
		if isJson:
			pat = '"snippet": "(.*?)",'
			with open(file_path,'r') as file:
				text = file.read()
			codes = re.compile(pat).findall(text)
		else:
			codes = []
			with open(file_path,'r') as file:
				for line in file:
					codes.append(line[:-1])
	except Exception as e:
		raise e
	return codes
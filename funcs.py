#coding:utf8

import re

def test(raw_code,db_codes=None,hp_tokens_text=None,TEST=False):
	code = replaceCode(raw_code) # 泛化代码
	tokens = code2tokens(code) # 提取tokens
	hp_tokens,lp_tokens = splitTokensByPRI(tokens) # 按优先级和顺序获取tokens
		
	hp_dict = generateDict(hp_tokens,text=hp_tokens_text,weight=50)
	
	# 获取 通过了高优先筛选的文本
	filt_text = ''
	for line_num in hp_dict.keys():
		filt_text+=db_codes[int(line_num)]+'\n'
		
	normal_dict = generateDict(tokens,dict=hp_dict,text=filt_text,weight=1)
	
	max_kvs = [] # 二维list
	for i in range(10):
		kv = [-1,0]
		max_kvs.append(kv)
	
	for key,value in normal_dict.items():
		for i in range(len(max_kvs)):
			if value[1] > max_kvs[i][1]:
				max_kvs.insert(i,[key,value[1]])
				max_kvs.pop(10)
				break
	
	return max_kvs[0]

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
	code = code.replace('\\n',' ')
	return code
	
# 通过tokens，对dict进行更新,weight是（用行次数表示）权重值，token越高优先，权重越大
def generateDict(tokens=[],text='',dict=None,weight=1):
	if dict == None:
		dict = {}
	# 正则匹配到的是 比如: 1203 print('Hello World')换行符 这样的一串文本内容和其行号数字
	pat_start = '(([0-9]+?) .*?'
	pat_end = '.*?\n)'
	pat_token = '([^0-9]*?)[0-9]*$'
	
	for token in tokens:
		token = re.compile(pat_token).findall(token)
		token = ''.join(token)
		
		if token in ['.','*','(',')','?','+','\\','[',']','{','}']:
			token = '\\'+token
			
		tmp_pat = token+'.*?'
		pat = pat_start+tmp_pat+pat_end
		r = re.compile(pat).findall(text)
		if len(r):
			pat_start+=tmp_pat
		
		for k in r:
			if k[1] in dict.keys():
				dict[ k[1] ][0] = k[0]
				dict[ k[1] ][1]+=weight
			else:
				# 初始化dict的键为某行数的值,为一个list,list[0]是爬到的文本,list[1]是行出现次数
				dict[ k[1] ] = [ k[0] , weight ]
	return dict
	
# 暂时通过文件读取（后面改成数据库
def getTextByNum(tokens,num_list):
	pass
	
# 输入tokens列表，返回按照优先级划分的2个list
def splitTokensByPRI(tokens,addNum=False):
	high_pri = ['.','(','['] # 这些字符前的词权重应该是最高的
	low_list = ['.','\'','"',' ','[',']','(',')','{','}',':','=',',','+','-','>','<','RONUM','ROSTRING','ROVAR','%']
	alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	
	hp_tokens = [] # 高优先级 tokens
	lp_tokens = [] # 低优先级 tokens
	
	length = len(tokens)
	
	if length:
		for i in range( 1,len(tokens) ):
			if addNum:
				token = tokens[i-1]+str(i-1)
			else:
				token = tokens[i-1]
			# 如果当前token是 .([中的一个，则前一个token优先级很高
			if tokens[i]  in high_pri and tokens[i-1] not in low_list and tokens[i-1] not in alpha_list:
				hp_tokens.append( token  )
			else:
				lp_tokens.append( token )
		if addNum:
			token = tokens[length-1]+str(length-1)
		else:
			token = tokens[length-1]
		lp_tokens.append( token ) # 将最后一项加入lp_tokens
	
	return hp_tokens,lp_tokens
	
# 获取两段code的相似度
# 泛化-转tokens- 计算 相似的token数 / 较长code的总token数
def getSimilarity(codeA,codeB):
	codeA = replaceCode(codeA)
	codeB = replaceCode(codeB)
	
	tokensA = code2tokens(codeA)
	tokensB = code2tokens(codeB)
	
	index_list = [] # 索引list
	
	# 求最长的相似token数（还要考虑顺序）
	
	# 第一步先按照tokensA的顺序求出所有在B中的token
	for token in tokensA: #遍历tokensA
		if token in tokensB:
			token_index = tokensB.index(token)
			index_list.append( token_index )
			tokensB[token_index] = '' # 将此处token置为空字符串，因为code2tokens不含''
	
	# 接下来求取index_list中递增且最长的一个离散序列的长度
	max = 0
	
	for i,index in enumerate(index_list):
		temp_max = 0
		for j in range( i+1, len(index_list) ):
			if index_list[j] > index:
				temp_max+=1
				index = index_list[j]
		if temp_max > max:
			max = temp_max
	
	try:
		tokens_num = len(tokensA)-1 if len(tokensA) > len(tokensB) else len(tokensB)-1
		r = max / tokens_num
	except Exception as e:
		r = 0
		print('[*] Data Error')
	return r
	
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
def generateTokensByPRI(codes,fileName='data/hp_tokens_id'):
	with open(fileName,'w') as file:
		for i,code in enumerate(codes):
			code = replaceCode(code)
			tokens = code2tokens(code)
			hp_tokens,lp_tokens = splitTokensByPRI(tokens)
			
			file.write( str(i)+' '+' '.join(hp_tokens)+'\n' )
			
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
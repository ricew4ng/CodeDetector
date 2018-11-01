#coding:utf8

from funcs import *

if __name__ == '__main__':
	# 生成高优先级tokens 文本 high_tokens_id
	# codes = getCodes('data/codes_train')
	# generateTokensByPRI(codes)
		
	# 载入高优先级库文本
	with open('data/high_tokens_id','r') as file:
		high_tokens_text = file.read()
		
	codes_train = []
	with open('data/codes_train','r') as file:
		for line in file:
			codes_train.append(line[:-1])
			
	# 输入待检测代码
	code = 'urllib.parse.unquote(\'Foo%E2%84%A2%20Bar\').decode(\'utf-8\')'
	
	tokens = code2tokens(code)
	
	h_tokens,l_tokens = splitTokensByPRI(tokens)
	
	dict = generateDict(h_tokens,text=high_tokens_text,weight=50)
	
	filt_text = ''
	
	for line_num in dict.keys():
		filt_text+=codes_train[int(line_num)]+'\n'
		
	dict = generateDict(l_tokens,text=filt_text,weight=0.1)
	
	max_kvs = [] # 二维list
	for i in range(10):
		kv = [-1,0]
		max_kvs.append(kv)
	
	for key,value in dict.items():
		for i in range(len(max_kvs)):
			if value[1] > max_kvs[i][1]:
				max_kvs.insert(i,[key,value[1]])
				max_kvs.pop(10)
				break
	
	print('[*] \tbase code=>'+code)
	for i in max_kvs:
		print( i[0]+' '+str(i[1])+'\tcode=>'+codes_train[int(i[0])] )
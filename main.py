#coding:utf8

from funcs import *
import json

if __name__ == '__main__':
	# 生成高优先级tokens 文本 high_tokens_id
	# codes = getCodes('data/codes_train')
	# generateTokensByPRI(codes,fileName='data/hp_tokens_id_train')
	# codes = getCodes('data/codes_test')
	# generateTokensByPRI(codes,fileName='data/hp_tokens_id_test')
		
	# 启用test库代码，否则用train库代码
	TEST = False
	
	if TEST:
		db_codes_path = 'data/codes_test_id'
		hp_tokens_text_path = 'data/hp_tokens_id_test'
	else:
		db_codes_path = 'data/codes_train_id'
		hp_tokens_text_path = 'data/hp_tokens_id_train'
	
	# 载入库代码
	db_codes = []
	with open(db_codes_path,'r') as file:
		for line in file:
			db_codes.append(line[:-1])
		
	# 载入高优先级库文本
	with open(hp_tokens_text_path,'r') as file:
		hp_tokens_text = file.read()
		
	
	code = 'matplotlib.rc(\'font\', **{\'sans-serif\': \'Arial\', \'family\': \'sans-serif\'})'
	code = 're.findall(\'\"(http.*?)\"\', s, re.MULTILINE | re.DOTALL)'
	index,weight = test(code,db_codes,hp_tokens_text,TEST)
	print(index,weight)
	print(db_codes[int(index)] )
	print(code)
	'''
	pat = '([0-9]+?) (.*)' # 提取正则式
	# 测试代码
	with open('./data/conala-test.json', 'r') as code_f:
		codes_org = code_f.read()
		codes_org = json.loads(codes_org)
		
		for i,code in enumerate(codes_org):
			code = code['snippet']
			index,weight = test(code,db_codes,hp_tokens_text,TEST)
			
			try:
				db_code_line,db_code = re.compile(pat).findall(db_codes[int(index)])[0]
			except:
				db_code_line = "-1"
				db_code = db_codes[int(index)]
				
			print('[*] base code\t=>\t'+code)
			print('[*] db code\t=>\t'+db_code+' Line=>'+db_code_line)
			print('[*] similarity\t=>\t'+str(getSimilarity(code,db_code)) )
			
			if i == 10: # 测试十条数据
				break
	'''
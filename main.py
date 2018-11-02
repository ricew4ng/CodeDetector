#coding:utf8

from funcs import *

if __name__ == '__main__':
	# 生成高优先级tokens 文本 high_tokens_id
	# codes = getCodes('data/codes_train')
	# generateTokensByPRI(codes,fileName='data/hp_tokens_id_train')
	# codes = getCodes('data/codes_test')
	# generateTokensByPRI(codes,fileName='data/hp_tokens_id_test')
		
	# 启用test库代码，否则用train库代码
	TEST = False
		
	# 输入待检测代码
	code = 'Point = namedtuple(\'whatsmypurpose\', [\'x\', \'y\'], verbose=True)'
		
		
	test(code,TEST)
	
	'''
	codes = [] # 多个数据测试
	
	for code in codes:
		test(code,TEST)
	'''
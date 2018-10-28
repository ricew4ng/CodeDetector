#coding:utf8

from funcs import *

# 最终目的是将库中每行代码对应一个向量，即生成一个向量矩阵存入文件中，还有一个dict
# 同时，测试代码要比较相似度的话，初始化一个全零list，需要通过一个dict，来给list相应位置1

# 如果要训练的话，就是看dict中是否有未知token，然后添加入dict中，并给list置1

# 现在已经能获取每行代码的token了

# 总结一下 语法树，一般来说
# 等号左边都是给某个变量赋值，所以可以把等号左边的变量都替换为某个定值
# 同

if __name__ == '__main__':
	codes = getCodes('./data/conala-train.json')
	
	print('[*] get codes ok')
	
	token_dict = {}
	vector = []
	
	vector_length = 0
	
	count = 0
	for code in codes:
		tokens = splitCode(code) # 获得此tokens
		token_dict,vector_length = trainDict(tokens,token_dict,vector_length)
		
	with open('output_dict','w') as file:
		for k,v in token_dict.items():
			file.write(k+'\t'+str(v)+'\n')
	
	
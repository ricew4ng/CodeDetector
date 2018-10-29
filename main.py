#coding:utf8

from funcs import *

# 最终目的是将库中每行代码对应一个向量，即生成一个向量矩阵存入文件中，还有一个dict
# 同时，测试代码要比较相似度的话，初始化一个全零list，需要通过一个dict，来给list相应位置1

# 如果要训练的话，就是看dict中是否有未知token，然后添加入dict中，并给list置1

# 总结一下 语法树，一般来说
# 等号左边都是给某个变量赋值，所以可以把等号左边的变量都替换为某个定值

if __name__ == '__main__':
	token_dict = getDict('data/output_dict') # 载入字典
	
	vector_length = 75162
	
	codes = getCodes('data/conala-train.json') # 载入raw代码
	
	print('[*] Training vectors...')
	
	vectorsA = [] # 初始化库中的vector数组
	
	
	count = 0 
	for code in codes:
		tokens = code2tokens(code) # 将代码转成token数组
		vector = tokens2vector(tokens,token_dict,vector_length)
		
		vectorsA.append(vector)
		count+=1
		if count == 50:
			break
		
		
	print('[*] VectorsA ready !')
	
	print('[*] Processing test codes...')
	
	codes = getCodes('data/conala-test.json') # 载入测试代码
	
	
	count = 0 # 测试3行代码
	
	for code in codes:
		tokens = code2tokens(code)
		vectorB = tokens2vector(tokens,token_dict,vector_length) #获取待测试代码的向量
		
		max_sim = 0
		
		# 遍历 vectorsA ，与vectorB做比较
		for vectorA in vectorsA:
			r = getCosine(vectorA,vectorB)
			if max_sim < r:
				max_sim = r
					
					
		print('[*] Result '+str(count+1)+'=>' +str(max_sim)+'\tcode=>'+' '.join(tokens))
		
		count+=1 
		if count == 20:
			break
	
	
	# x = map(lambda i:str(i) ,x )
	
	# with open('test','w') as file:
		# file.write( ','.join(x)+'\n' )
		
		
	'''# 训练token字典，比较耗时，几十秒左右
	codes = getCodes('./data/conala-train.json')
	
	vector_length = 0
	
	for code in codes:
		tokens = code2tokens(code) # 获得此tokens
		token_dict,vector_length = trainDict(tokens,token_dict,vector_length)
	
	with open('output_dict','w') as file:
		for k,v in token_dict.items():
			file.write(k+'\t'+str(v)+'\n')
	'''
#coding:utf8

from funcs import *
''' 
新的方法：
1. 先将conala-test.json的代码用 replaceCode方法保证语义不变的情况下，替换成相对"泛化"一点的代码，暂时保存在文件里
		
2. 然后对于一段输入的代码，做以下操作:

	a) 先把字符串，普通变量名之类的常量做替换，
	b) 用code2tokens函数切割代码为一个个token组成的list
	c) 遍历这个token_list，每次用正则在文件中匹配有这个token的行代码，返回行序号
	d) 对于每个token，都有一个由行序号组成的list
	e) 对这些list，找出它们之间的重合度最高的（就是这个token_list里的token在哪一行代码里出现的最多），生成一个dict，键是行序号，值是次数
	f) 也就是 次数越大，就跟目标代码越相似
	
	注: 考虑可以优化的地方，就是token的优先级。
'''

if __name__ == '__main__':
	with open('tokens_test','r') as file:
		text = file.read()
	
	# 测试代码：
	code = 'x = int(my_string.replace("ROSTRING", ""))'
	code = replaceCode(code)
	tokens = code2tokens(code)
	
	dict = {}
	for token in tokens:
		try:
			pat = '([0-9]+?) .*?'+token+'.*?\n'
			r = re.compile(pat).findall(text)
		except:
			pat = '([0-9]+?) .*?\\'+token+'.*?\n'
			r = re.compile(pat).findall(text)
			
		for i in r:
			if i in dict.keys():
				dict[i]+=1
			else:
				dict[i] = 1
	
	max_kvs = [] # 二维list
	for i in range(5):
		kv = [-1,0]
		max_kvs.append(kv)
	
	for key,value in dict.items():
		for i in range(len(max_kvs)):
			if value > max_kvs[i][1]:
				max_kvs.insert(i,[key,value])
				max_kvs.pop(5)
				break
	
	for i in max_kvs:
		print( i[0],i[1] )
	
	
	
	# codes_train = getCodes('data/conala-train.json')
	'''
	codes_test = getCodes('data/conala-test.json')
	
	with open('tokens_test','w') as file:
		for i,code in enumerate(codes_test):
			code = replaceCode(code)
			file.write(str(i)+' '+code+'\n' )
	'''
	
	
	
	'''
	with open('data/codes_test','w') as file:
		for i,code in enumerate(codes_test):
			file.write(str(i)+' '+code+'\n' )
			
	with open('tokens_test','w') as file:
		for i,code in enumerate(codes_test):
			tokens = code2tokens(code)
			file.write(str(i)+' '+' '.join(tokens)+'\n' )
	'''
#coding:utf8

import re

with open('test.json','r') as file:
	text = file.read()
	
pat = '"snippet": "(.*?)"'

r = re.compile(pat).findall(text)

for i in r:
	print(i)
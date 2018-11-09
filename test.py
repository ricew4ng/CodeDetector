

import re
from funcs import *


codeA = 'all(x == myList[0] for x in myList)'
codeB = 're.findall(\'\"(http.*?)\"\', s, re.MULTILINE | re.DOTALL)'

print( code2tokens(codeB) )


# str = '''4923 print(' '.join(get_words(['k', 'c', 't', 'a'])))'''

# pat = '([0-9]+?) (.*)'

# r = re.compile(pat).findall(str)

# print(r)
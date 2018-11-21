import astor

import ast


class CodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print( type(node).__name__ )
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print( type(node).__name__ )
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print( type(node).__name__ )
        ast.NodeVisitor.generic_visit(self, node)

code1 = 'a=123'
code2 = '''res = {k: v for k, v in list(kwargs.items()) if v is not None}'''

tree1 = ast.parse(code1)
tree2 = ast.parse(code2)

import re

pat = 'id=\'(.*?)\''

r = re.compile(pat).findall( ast.dump(tree2) )

print(r)



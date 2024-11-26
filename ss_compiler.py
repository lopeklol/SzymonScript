# Libraries
from os.path import dirname
import sys
import os
from typing import Optional
from json import load, dump
from random import randint

# Definitions of syntax
DEFINITONS = {
    'escape_character': '\\',
    'whitespaces': [' ', '\n'],
    'string_signs': ['"', "'", "`"],
    'comments': {
        'one_line': '//',
        'multi_line': {
            'start': '/*',
            'end': '*/',
        },
    },
    'syntaxes': {
        'separators': {
            ".": ".",
            ";": ";",
            ",": ",",
        },
        'brackets': {
            "(": "(",
            ")": ")",
            "[": "[",
            "]": "]",
            "{": "{",
            "}": "}",
        },
        'arithmetic_operators': {
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "++": "++",
            "--": "--",
        },
        'logical_operators': {
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "==": "==",
            "!=": "!=",
        },
        'other_operators': {
            "=": "=",
        },
        'boolean_operators': {
            "!": "!",
        },
    },
    'keywords': {
        'in-loop_keywords': {
            "break": "break",
            "continue": "continue",
        },
        'loops_keywords': {
            "if": "if",
            "else": "else",
            "for": "for",
            "while": "while",
        },
        'function_and_classes_keywords': {
            "def": "def",
            "class": "class",
        },
        'boolean_keywords': {
            "and": "and",
            "or": "or",
        },
        'other_keywords': {
            "in": "in",
            "as": "as",
        },
    }
}

# Getting the file to compile
if getattr(sys, 'frozen', False):
    path = dirname(sys.executable)
else:
    path = dirname(os.path.abspath(__file__))
file_name = input("Wprowadź nazwe pliku, który ma zostac skompilowany (bez rozszerzenia, przyjmuje tylko rozszerzenia .sex): ")
with open(f'{path}\\{file_name}.sex', 'r') as file:
    contents = file.read()
    file.close()

def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None

def find_longest_syntax() -> tuple:
    longest_len = 0
    longest_idx = 0
    for i, syntax in enumerate(SYNTAXES):
        if len(syntax) > longest_len:
            longest_len = len(syntax)
            longest_idx = i
    return (SYNTAXES[longest_idx], longest_idx, longest_len)

def find_longest_keyword() -> tuple:
    longest_len = 0
    longest_idx = 0
    for i, keyword in enumerate(KEYWORDS):
        if len(keyword) > longest_len:
            longest_len = len(keyword)
            longest_idx = i
    return (KEYWORDS[longest_idx], longest_idx, longest_len)

def find_syntax(contents, idx, max_length) -> tuple:
    for i in range(max_length, 0, -1):
        if contents[idx : idx + i] in SYNTAXES:
            return (True, contents[idx : idx + i])
    return (False, None)

def find_keyword(contents, idx, max_length) -> tuple:
    if idx - 1 >= 0 and not (contents[idx - 1] in SYNTAXES or contents[idx - 1] in WHITESPACES):
        return (False, None)
    for i in range(max_length, 0, -1):
        if contents[idx : idx + i] in KEYWORDS and (contents[idx + i] in SYNTAXES or contents[idx + i] in WHITESPACES):
            return (True, contents[idx : idx + i])
    return (False, None)

def raise_exception(*value, type: str = 'BaseException', line: int = 1, content_lines: str = contents.split(';')):
    text = ''
    for i in value:
        text += i + ' '
    text = text[:-1]
    print(f'''\nSzymonScript raised an exception in line {line}:\n
{content_lines[line - 1].strip()}\n
{type}: {text}.
''')
    input("Press [ENTER] key to close the compiler...")
    exit()

def delete_whitespaces(string: str):
    new = ''
    for i in string:
        if i in WHITESPACES:
            continue
        new += i
    return new

# Creating syntax/keywords/whitespaces/comments arrays
WHITESPACES = DEFINITONS['whitespaces']
SYNTAXES = [j for i in DEFINITONS['syntaxes'].values() for j in i.values()]
KEYWORDS = [j for i in DEFINITONS['keywords'].values() for j in i.values()]
STRING_SIGNS = DEFINITONS['string_signs']
LONGEST_SYNTAX_LENGTH = find_longest_syntax()[2]
LONGEST_KEYWORD_LENGTH = find_longest_keyword()[2]
COMMENTS = [DEFINITONS['comments']['one_line'], DEFINITONS['comments']['multi_line']['start'], DEFINITONS['comments']['multi_line']['end']]

# Printing settings
print('Using settings:')
print(f'Syntaxes: {SYNTAXES}')
print(f'Keywords: {KEYWORDS}')
print(f'Whitespaces: {WHITESPACES}')
print(f'Comments signs: {COMMENTS}')

# Tokenizing
tokens = []
inString = False
escape = False
current_token = ''
skip = 0
for idx, i in enumerate(contents):
    if skip > 0:
        skip -= 1
        continue
    if escape:
        current_token += i
        escape = False
        continue
    if contents[idx : idx + len(COMMENTS[0])] == COMMENTS[0]:
        try:
            while contents[idx + skip] != '\n':
                skip += 1
        except IndexError:
            break
        continue
    if contents[idx : idx + len(COMMENTS[1])] == COMMENTS[1]:
        try:
            while contents[idx + skip : idx + skip + len(COMMENTS[2])] != COMMENTS[2]:
                skip += 1
        except IndexError:
            break
        skip += 1
        continue
    if i in STRING_SIGNS:
        if inString:
            inString = False
            current_token += i
            if current_token != '':
                tokens.append(current_token)
            current_token = ''
        else:
            current_token = i
            inString = i
        continue
    if inString:
        if i == DEFINITONS['escape_character']:
            escape = True
        current_token += i
        continue
    if i in WHITESPACES:
        continue
    keyword = find_keyword(contents, idx, LONGEST_KEYWORD_LENGTH)
    if keyword[0]:
        if current_token != '':
            tokens.append(current_token)
        current_token = ''
        tokens.append(keyword[1])
        skip = len(keyword[1]) - 1
        continue
    syntax = find_syntax(contents, idx, LONGEST_SYNTAX_LENGTH)
    if syntax[0]:
        if current_token != '':
            tokens.append(current_token)
        current_token = ''
        tokens.append(syntax[1])
        skip = len(syntax[1]) - 1
        continue
    current_token += i

# Printing tokens
print(f"\nTokens: {tokens}")

# Saving tokens in file
with open('output.tokens', 'w') as result_file:
    result_file.write(str(tokens))
    result_file.close()

# Node class
class Node():
    def __init__(self, type: str = 'main', value: str = '', childs: list = None):
        self.type = type
        self.value = value
        self.childs = childs if childs is not None else []

    def add_child(self, type: str = 'main', value: str = '', childs: list = None):
        new_obj = Node(
            type=type,
            value=value,
            childs=childs if childs is not None else []
        )
        self.childs.append(new_obj)

def get_token_parent(program: Node, layers: int) -> Node:
    current = program
    try:
        for _ in range(layers):
            current = current.childs[-1]
    except SyntaxError:
        return program
    return current

def get_token_before(program: Node, layers: int) -> Node:
    current = program
    try:
        for _ in range(layers):
            current = current.childs[-1]
        current = current.childs[-1]
    except SyntaxError:
        return program
    return current

def modify_token_before(program: Node, layers: int, type: str = None, value: str = None, childs: list = None) -> None:
    current = program
    try:
        for _ in range(layers):
            current = current.childs[-1]
        current = current.childs[-1]
    except SyntaxError:
        current = program
    if type != None:
        current.type = type
    if value != None:
        current.value = value
    if childs != None:
        current.childs = childs

def tree_to_json(tree: Node):
    reasult = {}
    reasult['type'] = tree.type
    reasult['value'] = tree.value
    reasult['childs'] = []
    for child in tree.childs:
        reasult['childs'].append(tree_to_json(child))
    return reasult

defined_variables = {}
defined_arrays = {}
defined_objects = {'window': 'object', 'document': 'object'}
predefined_objects = ['window', 'document']

def get_variable_type(variable: str, defined_variables = defined_variables, defined_arrays = defined_arrays, defined_objects = defined_objects) -> str:
    # Types: Number, String, Array, Object
    if not variable in defined_variables and not variable in defined_arrays and not variable in defined_objects:
        raise_exception(f'Variable "{variable}" is not defined', type = 'ValueError', line = line)
    if not variable in defined_variables and variable in defined_arrays:
        return 'array'
    if not variable in defined_variables and variable in defined_objects:
        return 'object'
    NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in str(defined_variables[variable]):
        if not i in NUMS:
            return 'string'
    return 'number'

# Creating AST tree
brackets = []
program = Node()
layers = 0
default_layer_settings = {
    'idx': 0,
    'in_if': False,
    'in_else': False,
    'in_for': False,
    'in_while': False,
}
layers_vars = {
    0: default_layer_settings.copy()
}

skip = 0
line = 1
curr_layer = layers
for idx, token in enumerate(tokens):
    try:
        prev_token = get_token_before(program, layers)
    except IndexError:
        try:
            prev_token = get_token_parent(program, layers)
        except:
            prev_token = Node()
    if skip > 0:
        skip -= 1
        continue
    if token == DEFINITONS['syntaxes']['separators'][';']:
        if brackets != []:
            raise_exception(f'Not closed bracket "{brackets[-1]}"', type = 'SyntaxError', line = line)
        current_token_parent = get_token_parent(program, layers)
        current_token_parent.add_child('new_line')
        line += 1
        continue
    if token == DEFINITONS['syntaxes']['separators'][',']:
        current_token_parent = get_token_parent(program, layers)
        if current_token_parent.type == 'array':
            continue
        elif current_token_parent.type == 'init':
            layers_vars.pop(layers)
            layers -= 1
            current_token_parent = get_token_parent(program, layers)
            current_token_parent.add_child('cond')
            layers += 1
            layers_vars[layers] = default_layer_settings.copy()
            continue
        elif current_token_parent.type == 'cond':
            layers_vars.pop(layers)
            layers -= 1
            current_token_parent = get_token_parent(program, layers)
            current_token_parent.add_child('increment')
            layers += 1
            layers_vars[layers] = default_layer_settings.copy()
            continue
        current_token_parent.add_child('separator', ',')
        continue
    if token == DEFINITONS['syntaxes']['separators']['.']:
        if prev_token.value[1:] in predefined_objects:
            modify_token_before(program, layers, value=prev_token.value[1:])
        current_token_parent.add_child('separator', '.')
        continue
    if token in [DEFINITONS['syntaxes']['brackets']['('],
                 DEFINITONS['syntaxes']['brackets'][')'],
                 DEFINITONS['syntaxes']['brackets']['['],
                 DEFINITONS['syntaxes']['brackets'][']']]:
        if token == DEFINITONS['syntaxes']['brackets']['(']:
            current_token_parent = get_token_parent(program, layers)
            if current_token_parent.type == 'condition_statement':
                if current_token_parent.value == 'else':
                    raise_exception(f'"Else" statement doesn\'t recive condition', type = 'SyntaxError', line = line)
                if current_token_parent.value == 'for':
                    current_token_parent.add_child('condition')
                    layers += 1
                    layers_vars[layers] = default_layer_settings.copy()
                    current_token_parent = get_token_parent(program, layers)
                    current_token_parent.add_child('init')
                else:
                    current_token_parent.add_child('condition')
            layers += 1
            layers_vars[layers] = default_layer_settings.copy()
            brackets.append(token)
        elif token == DEFINITONS['syntaxes']['brackets']['[']:
            current_token_parent = get_token_parent(program, layers)
            if get_token_before(program, layers).type == 'set_operator':
                current_token_parent.add_child('array')
            else:
                current_token_parent.add_child('index')
            layers += 1
            layers_vars[layers] = default_layer_settings.copy()
            brackets.append(token)
        else:
            try:
                if not (token == DEFINITONS['syntaxes']['brackets'][')'] and
                        brackets[-1] == DEFINITONS['syntaxes']['brackets']['('] or
                        token == DEFINITONS['syntaxes']['brackets'][']'] and
                        brackets[-1] == DEFINITONS['syntaxes']['brackets']['[']):
                    raise_exception(f'Not opened bracket "{token}"', type = 'SyntaxError', line = line)
                if get_token_parent(program, layers).type == 'condition' and token == DEFINITONS['syntaxes']['brackets'][')']:
                    layers_vars.pop(layers)
                    layers -= 1
                    current_token_parent = get_token_parent(program, layers)
                    current_token_parent.add_child('body')
                elif get_token_parent(program, layers).type == 'increment' and token == DEFINITONS['syntaxes']['brackets'][')']:
                    layers_vars.pop(layers)
                    layers -= 1
                    layers_vars.pop(layers)
                    layers -= 1
                    current_token_parent = get_token_parent(program, layers)
                    current_token_parent.add_child('body')
                else:
                    layers_vars.pop(layers)
                    layers -= 1
                brackets.pop()
            except:
                raise_exception(f'Not opened bracket "{token}"', type = 'SyntaxError', line = line)
        continue
    if token == DEFINITONS['syntaxes']['brackets']['{']:
        layers += 1
        layers_vars[layers] = default_layer_settings.copy()
        continue
    if token == DEFINITONS['syntaxes']['brackets']['}']:
        for i in DEFINITONS['keywords']['loops_keywords'].values():
            if layers_vars[layers][f'in_{i}']:
                layers_vars[layers][f'in_{i}'] = False
        layers_vars.pop(layers)
        layers -= 1
        layers_vars.pop(layers)
        layers -= 1
        if layers < 0:
            raise_exception('Not opened bracket "{"', type = 'SyntaxError', line = line)
        continue
    if token in DEFINITONS['keywords']['loops_keywords'].values():
        current_token_parent = get_token_parent(program, layers)
        current_token_parent.add_child('condition_statement', get_key_by_value(DEFINITONS['keywords']['loops_keywords'], token))
        if get_key_by_value(DEFINITONS['keywords']['loops_keywords'], token) == 'else':
            current_token_parent.childs[-1].add_child('body')
        x = get_key_by_value(DEFINITONS['keywords']['loops_keywords'], token)
        layers_vars[layers][f'in_{x}'] = True
        del x
        layers += 1
        layers_vars[layers] = default_layer_settings.copy()
        continue
    current_token_parent = get_token_parent(program, layers)
    if token in [i for i in DEFINITONS['syntaxes']['arithmetic_operators'].values()]:
        if not (prev_token.type in ['variable', 'string', 'integer', 'array'] or prev_token.type == DEFINITONS['syntaxes']['brackets'][')']) and token == DEFINITONS['syntaxes']['arithmetic_operators']['+']:
            current_token_parent.add_child('probably_positive_integer', '+')
        elif prev_token.type != 'variable' and token == DEFINITONS['syntaxes']['arithmetic_operators']['-']:
            current_token_parent.add_child('probably_negative_integer', '-')
        else:
            current_token_parent.add_child('arithmetic_operator', get_key_by_value(DEFINITONS['syntaxes']['arithmetic_operators'], token))
    elif token == DEFINITONS['syntaxes']['other_operators']['=']:
        current_token_parent.add_child('set_operator', get_key_by_value(DEFINITONS['syntaxes']['other_operators'], token))
    elif token in [i for i in DEFINITONS['syntaxes']['logical_operators'].values()]:
        current_token_parent.add_child('logical_operator', get_key_by_value(DEFINITONS['syntaxes']['logical_operators'], token))
    elif token in [DEFINITONS['syntaxes']['boolean_operators']['!']] + [i for i in DEFINITONS['keywords']['boolean_keywords'].values()]:
        if token == DEFINITONS['syntaxes']['boolean_operators']['!']:
            current_token_parent.add_child('boolean_operator', '!')
        else:
            current_token_parent.add_child('boolean_operator', get_key_by_value(DEFINITONS['keywords']['boolean_keywords'], token))
    else:
        try:
            if prev_token.type == 'probably_positive_integer':
                modify_token_before(program, layers, 'positive_integer')
                current_token_parent.add_child('integer', float(token))
            elif prev_token.type == 'probably_negative_integer':
                modify_token_before(program, layers, 'negative_integer')
                current_token_parent.add_child('integer', float(token)*-1)
            else:
                raise ValueError
        except ValueError:
            try:
                if token[0] in STRING_SIGNS and token[-1] == token[0]:
                    current_token_parent.add_child('string', token)
                elif tokens[idx + 1] == DEFINITONS['syntaxes']['brackets']['(']:
                    current_token_parent.add_child('function', token)
                else:
                    try:
                        if tokens[idx + 1] == '=':
                            defined_variables[token] = ''
                    except IndexError:
                        pass
                    defined = [i for i in defined_variables.keys()] + [i for i in defined_arrays.keys()] + [i for i in defined_objects.keys()]
                    if token not in defined:
                        raise_exception(f'Undefined variable "{token}"', type = 'NameError', line = line)
                    current_token_parent.add_child('variable', f'_{token}')
            except SyntaxError:
                try:
                    if tokens[idx + 1] == '=':
                        defined_variables[token] = ''
                except IndexError:
                    pass
                defined = [i for i in defined_variables.keys()] + [i for i in defined_arrays.keys()] + [i for i in defined_objects.keys()]
                if token not in defined:
                    raise_exception(f'Undefined variable "{token}"', type = 'NameError', line = line)
                current_token_parent.add_child('variable', f'_{token}')
    layers_vars[layers]['idx'] += 1

with open('tree.json', 'w') as tree_file:
    dump(tree_to_json(program), tree_file, indent = 4)
    tree_file.close()

# Creating JS code
code_tokens = []
line = 1
def generate_js(node):
    global line
    if node.type == 'main':
        value = ''.join([generate_js(i) for i in node.childs])
        return f'{value}'
    
    elif node.type == 'separator':
        return node.value
    
    elif node.type == 'positive_integer':
        return node.value

    elif node.type == 'negative_integer':
        return node.value

    elif node.type == 'other_operator':
        return node.value
    
    elif node.type == 'variable':
        return node.value
    
    elif node.type == 'integer':
        return str(node.value)
    
    elif node.type == 'string':
        return node.value
    
    elif node.type == 'arithmetic_operator':
        return node.value
    
    elif node.type == 'logical_operator':
        return node.value
    
    elif node.type == 'boolean_operator':
        return node.value
    
    elif node.type == 'function':
        function_name = node.value
        args = ''.join(generate_js(child) for child in node.childs)
        return f"{function_name}({args})"
    
    elif node.type == 'array':
        elements = ", ".join(generate_js(child) for child in node.childs)
        return f"[{elements}]"
    
    elif node.type == 'condition_statement':
        if node.value == 'else':
            body = generate_js(node.childs[0])
            return f"else {{\n {body} }}"
        condition = generate_js(node.childs[0])
        body = generate_js(node.childs[1])
        if node.value == 'if':
            return f"if ({condition}) {{\n {body} }}"
        elif node.value == 'while':
            return f"while ({condition}) {{\n {body} }}"
        elif node.value == 'for':
            init = generate_js(node.childs[0].childs[0])
            cond = generate_js(node.childs[0].childs[1])
            increment = generate_js(node.childs[0].childs[2])
            return f"for ({init}; {cond}; {increment}) {{\n {body} }}"
    
    elif node.type == 'condition':
        elements = "".join(generate_js(child) for child in node.childs)
        return f"{elements}"
    
    elif node.type == 'init':
        elements = "".join(generate_js(child) for child in node.childs)
        return f"{elements}"
    
    elif node.type == 'cond':
        elements = "".join(generate_js(child) for child in node.childs)
        return f"{elements}"
    
    elif node.type == 'increment':
        elements = "".join(generate_js(child) for child in node.childs)
        return f"{elements}"
    
    elif node.type == 'body':
        elements = "".join(generate_js(child) for child in node.childs)
        return f"{elements}"

    elif node.type == 'set_operator':
        return node.value
    
    elif node.type == 'new_line':
        line += 1
        return ';\n'
    
    elif node.type == 'index':
        x = "".join(generate_js(child) for child in node.childs)
        return f'[{x}]'
    
    else:
        return ""

code = generate_js(program)
print(f'\nCompiled code:\n\n{code}\n')

with open(f'{file_name}.js', 'w') as code_file:
    code_file.write(code)
    code_file.close()

input("Press [ENTER] key to close the compiler...")
exit()
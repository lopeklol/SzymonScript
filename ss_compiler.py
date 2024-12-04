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
            ".": "->",
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
            "function": "define_function",
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

# Function definitions
FUNCTIONS = {
    'console': {
        'type': 'object',
        'name': 'console',
        'call_keyword': 'console',
        'childs': {
            'log': {
                'type': 'method',
                'name': 'log',
                'call_keyword': 'print',
                'value': None
            },
            'error': {
                'type': 'method',
                'name': 'error',
                'call_keyword': 'error',
                'value': None
            },
            'warn': {
                'type': 'method',
                'name': 'warn',
                'call_keyword': 'warn',
                'value': None
            }
        }
    },
    'Math': {
        'type': 'object',
        'name': 'Math',
        'call_keyword': 'Math',
        'childs': {
            'add': {
                'type': 'method',
                'name': 'add',
                'call_keyword': 'add',
                'value': None
            },
            'subtract': {
                'type': 'method',
                'name': 'subtract',
                'call_keyword': 'subtract',
                'value': None
            },
            'multiply': {
                'type': 'method',
                'name': 'multiply',
                'call_keyword': 'multiply',
                'value': None
            },
            'divide': {
                'type': 'method',
                'name': 'divide',
                'call_keyword': 'divide',
                'value': None
            },
            'random': {
                'type': 'method',
                'name': 'random',
                'call_keyword': 'random',
                'value': None
            },
            'round': {
                'type': 'method',
                'name': 'round',
                'call_keyword': 'round',
                'value': None
            }
        }
    },
    'Array': {
        'type': 'object',
        'name': 'Array',
        'call_keyword': 'Array',
        'childs': {
            'sort': {
                'type': 'method',
                'name': 'sort',
                'call_keyword': 'sort',
                'value': "Array.prototype.sort = function() {\nreturn Array.prototype.sort.call(this, (a, b) => {\nif (a < b) return -1;\nif (a > b) return 1;\nreturn 0;});\n};"
            },
            'filter': {
                'type': 'method',
                'name': 'filter',
                'call_keyword': 'filter',
                'value': None
            },
            'map': {
                'type': 'method',
                'name': 'map',
                'call_keyword': 'map',
                'value': None
            },
            'push': {
                'type': 'method',
                'name': 'push',
                'call_keyword': 'push',
                'value': None
            },
            'pop': {
                'type': 'method',
                'name': 'pop',
                'call_keyword': 'pop',
                'value': None
            }
        }
    },
    'Object': {
        'type': 'object',
        'name': 'Object',
        'call_keyword': 'Object',
        'childs': {
            'keys': {
                'type': 'method',
                'name': 'keys',
                'call_keyword': 'keys',
                'value': None
            },
            'values': {
                'type': 'method',
                'name': 'values',
                'call_keyword': 'values',
                'value': None
            },
            'entries': {
                'type': 'method',
                'name': 'entries',
                'call_keyword': 'entries',
                'value': None
            }
        }
    },
    'String': {
        'type': 'object',
        'name': 'String',
        'call_keyword': 'String',
        'childs': {
            'length': {
                'type': 'method',
                'name': 'length',
                'call_keyword': 'length',
                'value': None
            },
            'toUpperCase': {
                'type': 'method',
                'name': 'toUpperCase',
                'call_keyword': 'toUpperCase',
                'value': None
            },
            'toLowerCase': {
                'type': 'method',
                'name': 'toLowerCase',
                'call_keyword': 'toLowerCase',
                'value': None
            }
        }
    }
}

# Getting the file to compile
if getattr(sys, 'frozen', False):
    path = dirname(sys.executable)
else:
    path = dirname(os.path.abspath(__file__))
file_name = input("Enter the file name to compile (write name without extension, accepts only \"*.sex\" files): ")
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
    except IndexError:
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
defined_objects = {}
defined_functions = {}

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

def check_if_function_exists(function_name: str, path: list = [], function_list: list = FUNCTIONS) -> bool:
    if path != []:
        for i in function_list.values():
            if i['call_keyword'] == path[0]:
                print(function_list, path)
                return check_if_function_exists(function_name, path[1:], function_list[i['name']]['childs'])
        return False
    for i in function_list.values():
        if i['call_keyword'] == function_name:
            if i['type'] == 'method':
                return {'result': True, 'type': 'method', 'name': i['name'], 'value': i['value']}
            return {'result': True, 'type': 'object', 'name': i['name'], 'childs': i['childs']}
    return {'result': False, 'type': None}

# Creating AST tree
brackets = []
program = Node()
layers = 0
functions_to_update = []
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
global_settings = {
    'current_path': [],
    'in_function_args': False,
    'in_function_body': False,
    'in_function_variables': [],
}

skip = 0
line = 1
curr_layer = layers
for idx, token in enumerate(tokens):
    with open('tree.json', 'w') as tree_file:
        dump(tree_to_json(program), tree_file, indent = 4)
        tree_file.close()
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
        if check_if_function_exists(tokens[idx - 1], global_settings['current_path'])['result']:
            global_settings['current_path'] = global_settings['current_path'] + [tokens[idx - 1]]
            continue
        print(global_settings['current_path'])
        raise_exception(f'Undefined object "{tokens[idx - 1]}"', type = 'NameError', line = line)
    if token in [DEFINITONS['syntaxes']['brackets']['('],
                 DEFINITONS['syntaxes']['brackets'][')'],
                 DEFINITONS['syntaxes']['brackets']['['],
                 DEFINITONS['syntaxes']['brackets'][']']]:
        if token == DEFINITONS['syntaxes']['brackets']['(']:
            current_token_parent = get_token_parent(program, layers)
            if current_token_parent.type == 'condition_statement' or prev_token.type in ['function_definition', 'class_definition']:
                if prev_token.type in ['function_definition', 'class_definition']:
                    current_token_parent.add_child('args')
                elif current_token_parent.value == 'else':
                    raise_exception(f'"Else" statement doesn\'t recive condition', type = 'SyntaxError', line = line)
                elif current_token_parent.value == 'for':
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
                if get_token_parent(program, layers).type == 'args':
                    layers_vars.pop(layers)
                    layers -= 1
                    global_settings['in_function_args'] = False
                    global_settings['in_function_body'] = True
                    current_token_parent = get_token_parent(program, layers)
                    current_token_parent.add_child('body')
                elif get_token_parent(program, layers).type == 'condition' and token == DEFINITONS['syntaxes']['brackets'][')']:
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
        if get_token_parent(program, layers).type == 'body':
            global_settings['in_function_body'] = False
            global_settings['in_function_variables'] = []
            layers_vars.pop(layers)
            layers -= 1
        else:
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
    elif token in [i for i in DEFINITONS['keywords']['function_and_classes_keywords'].values()]:
        current_token_parent.add_child('define_keyword', get_key_by_value(DEFINITONS['keywords']['function_and_classes_keywords'], token))
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
                func = check_if_function_exists(token, global_settings['current_path'])
                if token[0] in STRING_SIGNS and token[-1] == token[0]:
                    current_token_parent.add_child('string', token)
                elif prev_token.type == 'define_keyword':
                    layers += 1
                    layers_vars[layers] = default_layer_settings.copy()
                    current_token_parent.add_child(f'{prev_token.value}_definition', get_key_by_value(DEFINITONS['keywords']['function_and_classes_keywords'], token))
                    global_settings['in_function_args'] = True
                elif tokens[idx + 1] == DEFINITONS['syntaxes']['brackets']['(']:
                    if func['type'] != 'method':
                        raise_exception(f'Undefined method: "{token}"', type = "NameError", line = line)
                    current_token_parent.add_child('function', func['name'])
                    if func['value']:
                        functions_to_update.append({
                            'name': func['name'],
                            'path': global_settings['current_path'],
                        })
                    global_settings['current_path'] = []
                elif func['result']:
                    current_token_parent.add_child('object', func['name'])
                else:
                    try:
                        if tokens[idx + 1] == '=':
                            current_token_parent.add_child('variable_definition', 'var')
                            defined_variables[token] = ''
                    except IndexError:
                        pass
                    defined = [i for i in defined_variables.keys()] + [i for i in defined_arrays.keys()] + [i for i in defined_objects.keys()]
                    if token not in defined and not global_settings['in_function_args'] and not (token in global_settings['in_function_variables'] and global_settings['in_function_body']):
                        x = 'object' if tokens[idx + 1] == DEFINITONS["syntaxes"]['separators']['.'] else 'variable'
                        raise_exception(f'Undefined {x} "{token}"', type = 'NameError', line = line)
                    if global_settings['in_function_args']:
                        global_settings['in_function_variables'] = global_settings['in_function_variables'] + [token]
                    current_token_parent.add_child('variable', f'_{token}')
            except IndexError:
                try:
                    if tokens[idx + 1] == '=':
                        defined_variables[token] = ''
                except IndexError:
                    pass
                defined = [i for i in defined_variables.keys()] + [i for i in defined_arrays.keys()] + [i for i in defined_objects.keys()]
                if token not in defined and not global_settings['in_function_args'] and not (token in global_settings['in_function_variables'] and global_settings['in_function_body']):
                    raise_exception(f'Undefined variable "{token}"', type = 'NameError', line = line)
                if global_settings['in_function_args']:
                    global_settings['in_function_variables'] = global_settings['in_function_variables'] + [token]
                current_token_parent.add_child('variable', f'_{token}')
    layers_vars[layers]['idx'] += 1

with open('tree.json', 'w') as tree_file:
    dump(tree_to_json(program), tree_file, indent = 4)
    tree_file.close()

# Creating JS code
code_tokens = []
line = 1

def generate_functions_overwrite():
    result = ''
    for i in functions_to_update:
        childs = FUNCTIONS
        for j in i['path']:
            childs = childs[j]['childs']
        string = childs[i['name']]['value']
        result += string + '\n'
    return result

def generate_js(node: Node):
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

    elif node.type == 'variable_definition':
        return node.value + ' '
    
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
    
    elif node.type == 'object':
        function_name = node.value
        return f"{function_name}."
    
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
    
    elif node.type == 'define_keyword':
        return f"{node.value} "
    
    elif node.type.endswith('_definition'):
        args = ''.join(generate_js(child) for child in node.childs[0].childs)
        body = generate_js(node.childs[1])
        return f"{node.value}({args}) {{\n {body} }}\n"

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

code = generate_functions_overwrite() + '\n' + generate_js(program)
print(f'\nCompiled code:\n\n{code}\n')

with open(f'{file_name}.js', 'w') as code_file:
    code_file.write(code)
    code_file.close()

input("Press [ENTER] key to close the compiler...")
exit()

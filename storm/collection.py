DIGITS = "0123456789"
PERIOD_SEPERATOR = "."

LOWER_CASE_ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
UPPER_CASE_ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABETS = LOWER_CASE_ALPHABETS + UPPER_CASE_ALPHABETS

OPERATORS = {
    '**': 'EXPONENT_OPERATOR',
    '//': 'FLOOR_DIVISION_OPERATOR',
    '==': 'EQUALITY_OPERATOR',
    '+': 'ADDITION_OPERATOR',
    '-': 'SUBTRACTION_OPERATOR',
    '*': 'MULTIPLICATION_OPERATOR',
    '/': 'DIVISION_OPERATOR',
    '=': 'ASSIGNMENT_OPERATOR',
}
INVERSE_OPERATORS = {OPERATORS[x]: x for x in OPERATORS}
BASE_OPERATORS = ['+', '-', '/', '*', '=']
OPERATOR_PRIORITY_ORDER = [
    ['**'],
    ['*', '/', '//'],
    ['+', '-'],
    ['==', '=']
]

PREFIXES = ['+', '-', '*']

STRING_PARENS = ["'", '"']
PRINT = '=>'
LINE_BREAK = ';'

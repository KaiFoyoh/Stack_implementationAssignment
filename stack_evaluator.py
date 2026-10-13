"""Evaluate arithmetic expressions with two explicit stacks (no eval())."""
from pathlib import Path
import re
import sys

TOKEN_PATTERN = re.compile(r'\d+(?:\.\d+)?|\.\d+|[()+*/-]')
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, 'u+': 3, 'u-': 3}


class Stack:
    """A last-in, first-out collection backed by a Python list."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise ValueError('Stack underflow: cannot pop an empty stack')
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise ValueError('Stack underflow: cannot peek at an empty stack')
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)


def tokenize(expression):
    if re.search(r'\d\s+\d', expression):
        raise ValueError('Missing operator between numbers')
    compact = re.sub(r'\s+', '', expression)
    if not compact:
        raise ValueError('Empty expression')
    tokens = TOKEN_PATTERN.findall(compact)
    if ''.join(tokens) != compact:
        raise ValueError('Invalid character or number in expression')
    return tokens


def apply_operator(values, operators):
    operator = operators.pop()
    if operator in ('u+', 'u-'):
        if len(values) < 1:
            raise ValueError('Missing operand for unary operator')
        number = values.pop()
        values.push(number if operator == 'u+' else -number)
        return
    if len(values) < 2:
        raise ValueError('Missing operand for binary operator')
    right, left = values.pop(), values.pop()
    if operator == '+':
        result = left + right
    elif operator == '-':
        result = left - right
    elif operator == '*':
        result = left * right
    elif operator == '/':
        if right == 0:
            raise ValueError('Division by zero')
        result = left / right
    else:
        raise ValueError(f'Unknown operator: {operator}')
    values.push(result)


def evaluate(expression):
    values, operators = Stack(), Stack()
    expect_operand = True
    for token in tokenize(expression):
        if token[0].isdigit() or token[0] == '.':
            if not expect_operand:
                raise ValueError('Missing operator before number')
            values.push(float(token))
            expect_operand = False
        elif token == '(':
            if not expect_operand:
                raise ValueError('Missing operator before opening parenthesis')
            operators.push(token)
        elif token == ')':
            if expect_operand:
                raise ValueError('Missing operand before closing parenthesis')
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator(values, operators)
            if operators.is_empty():
                raise ValueError('Unmatched closing parenthesis')
            operators.pop()
            expect_operand = False
        else:
            if expect_operand:
                if token not in ('+', '-'):
                    raise ValueError('Missing left operand')
                operators.push('u+' if token == '+' else 'u-')
            else:
                while (not operators.is_empty() and operators.peek() != '(' and
                       (PRECEDENCE[operators.peek()] > PRECEDENCE[token] or
                        (PRECEDENCE[operators.peek()] == PRECEDENCE[token]))):
                    apply_operator(values, operators)
                operators.push(token)
                expect_operand = True
    if expect_operand:
        raise ValueError('Expression ends with an operator or is incomplete')
    while not operators.is_empty():
        if operators.peek() == '(':
            raise ValueError('Unmatched opening parenthesis')
        apply_operator(values, operators)
    if len(values) != 1:
        raise ValueError('Malformed expression')
    return values.pop()


def format_result(number):
    if number.is_integer():
        return str(int(number))
    return format(number, '.12g')


def process_file(input_path='input.txt', output_path='output.txt'):
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(f'Input file not found: {source}')
    output_lines = []
    for line_number, line in enumerate(source.read_text(encoding='utf-8').splitlines(), 1):
        stripped = line.strip()
        if not stripped or re.fullmatch(r'-{3,}', stripped):
            output_lines.append(line)
            continue
        try:
            output_lines.append(format_result(evaluate(stripped)))
        except ValueError as exc:
            output_lines.append(f'ERROR (line {line_number}): {exc}')
    Path(output_path).write_text('\n'.join(output_lines) + '\n', encoding='utf-8')
    return len(output_lines)


if __name__ == '__main__':
    try:
        count = process_file(*(sys.argv[1:3]))
        print(f'Processed {count} lines. Results saved to {sys.argv[2] if len(sys.argv) > 2 else "output.txt"}')
    except (FileNotFoundError, OSError) as error:
        print(f'File error: {error}', file=sys.stderr)
        sys.exit(1)

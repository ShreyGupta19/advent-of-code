import re

from sly import Lexer, Parser

from advent import AdventProblem


def preprocess(line):
    line = ''.join(line.split())
    tokens = re.findall(r'\d+|\(|\)|\+|\-|\*|\/', line)
    return tokens

def run_op(n1, n2, op):
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        return n1 / n2
    elif op == None:
        return n2

def part_1(stmts):
    total = 0
    for stmt in stmts:
        num_stack = [None]
        ops_stack = [None]
        for token in stmt:
            if token.isdigit():
                token = int(token)
                if num_stack[-1] is None:
                    num_stack[-1] = token
                else:
                    num_stack[-1] = run_op(num_stack[-1], token, ops_stack[-1])
            elif token in ('+', '-', '*', '/'):
                ops_stack[-1] = token
            elif token == '(':
                num_stack.append(None)
                ops_stack.append(None)
            elif token == ')':
                right = num_stack.pop()
                ops_stack.pop()
                num_stack[-1] = run_op(num_stack[-1], right, ops_stack[-1])
        total += num_stack[-1]
    return total


class CalcLexer(Lexer):
    tokens = { NUMBER, PLUS, TIMES, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    TIMES = r'\*'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', TIMES),
        ('left', PLUS),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)


def part_2(inputs):
    lexer = CalcLexer()
    parser = CalcParser()
    total = 0
    for input in inputs:
        total += parser.parse(lexer.tokenize(input))
    return total


if __name__ == '__main__':
    part1 = AdventProblem(18, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(18, 2, lambda x: x)
    part2.add_solution(part_2)
    part2.run()

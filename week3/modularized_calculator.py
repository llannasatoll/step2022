"""
step2022 -week3-
モジュール化を意識して、括弧に対応した電卓プログラムを作ろう
"""

def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index

def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_times(line, index):
  token = {'type': 'TIMES'}
  return token, index + 1

def read_divide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_times(line, index)
    elif line[index] == '/':
      (token, index) = read_divide(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)

  return tokens


def remove_caluculated(tokens, index):
  tokens.pop(index)
  tokens.pop(index)


def evaluate_minus(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]["type"] == "MINUS":
      if not (tokens[index-1]["type"] == "NUMBER"):
        tokens.insert(index, {'type': 'NUMBER', 'number': -1*tokens[index+1]["number"]})
        remove_caluculated(tokens, index+1)
    index += 1
  return tokens


def evaluate_multiply_divied(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'TIMES':
      tmp = tokens[index-1]['number'] * tokens[index+1]['number']
    elif tokens[index]['type'] == 'DIVIDE':
      tmp = tokens[index-1]['number'] / tokens[index+1]['number']
    else:
      index += 1
      continue
    tokens[index-1]['number'] = tmp
    remove_caluculated(tokens, index)
  return tokens


def evaluate_add_subtract(tokens):
  answer = 0
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def evaluate(line):
  tokens = tokenize(line)
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  tokens = evaluate_minus(tokens)
  tokens = evaluate_multiply_divied(tokens)
  actual_answer = evaluate_add_subtract(tokens)
  return actual_answer


def my_calculator(line):
  i = 0
  while i < len(line):
    if line[i] == "(":
      start_index = i
    elif line[i] == ")":
      line = line[:start_index] + str(evaluate(line[start_index+1:i])) + line[i+1:]
      i = -1
    i += 1
  return evaluate(line)


def test(line):
  actual_answer = my_calculator(line)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("3")
  test("1+2")
  test("1.0+2.1-3")
  test("2*3")
  test("2*10*3/2/5")
  test("1.0*2-3.2/4+1")
  test("(1+2)")
  test("(1+(2*3))-(2.0/4)")
  test("2+2*3/(1-3.0)")
  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  answer = my_calculator(line)
  print("answer = %f\n" % answer)

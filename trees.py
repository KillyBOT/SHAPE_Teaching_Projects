import re, sys

operators = ("+","-","*","/","^","(")
operatorImportanceIn = {"+" : 2, "-" : 2, "*" : 4, "/" : 4, "(" : 0, "^" : 5}
operatorImportanceOut = {"(" : 7, "-" : 1, "+" : 1, "/" : 3, "*" : 3, "^" : 6}

class Node:

	def __init__(self, data, left = None, right = None):
		self.left = left
		self.right = right
		self.data = data

	def __repr__(self):
		return str(self.left) + "," + str(self.right) + "," + self.data

class ExpNode(Node):

	def __init__(self, data, left = None, right = None):
		Node.__init__(self,data,left,right)

	def evaluate(self):
		leftVal = 0
		rightVal = 0

		if type(self.left) != ExpNode:
			leftVal = float(self.left)
		else:
			leftVal = self.left.evaluate()

		if type(self.right) != ExpNode:
			rightVal = float(self.right)
		else:
			rightVal = self.right.evaluate()

		if self.data == "+":
			return leftVal + rightVal
		elif self.data == "-":
			return leftVal - rightVal
		elif self.data == "*":
			return leftVal * rightVal
		elif self.data == "/":
			return leftVal / rightVal
		else:
			return leftVal ** rightVal

def infixToPostfix(infixNotation):
	stack = []
	postfixNotation = ""
	tokens = re.split('(\+|\-|\*|\/|\^|\(|\))',infixNotation)

	for token in tokens:
		if(token == ""):
			pass
		elif token not in operators and token != ")":
			postfixNotation += token + ","

		elif token in operators:
			if len(stack) == 0:
				stack.append(token)
			elif operatorImportanceOut[token] > operatorImportanceIn[stack[-1]]:
				stack.append(token)
			else:
				while len(stack) > 0 and operatorImportanceOut[token] < operatorImportanceIn[stack[-1]]:
					postfixNotation += stack.pop() + ","
				stack.append(token)
		elif token == ")":
			while stack[-1] != "(":
				postfixNotation += stack.pop() + ","
			stack.pop()
	while len(stack) > 0:
		postfixNotation += stack.pop() + ","

	postfixNotation = postfixNotation[:-1]
	return postfixNotation

class ExpTree:
	def __init__(self, postfixNotation):
		self.tokens = postfixNotation.split(",")

		stack = []

		for token in self.tokens:
			if token not in operators:
				stack.append(token)
			else:
				rightVal = stack.pop()
				leftVal = stack.pop()
				stack.append(ExpNode(token,leftVal,rightVal))

		self.rootNode = stack.pop()

	def __repr__(self):
		return str(self.rootNode)

	def evaluate(self):
		return self.rootNode.evaluate()

def evaluate(toEval):
	postfixNotation = infixToPostfix(toEval)
	tree = ExpTree(postfixNotation)
	return tree.evaluate()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit()
	else:
		print(evaluate(sys.argv[1]))
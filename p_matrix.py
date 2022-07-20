import random

def matrix_25():
	array = [
	[],[],[],[],[]
	]

def gen_row():
	row = []
	for i in range(0,5):
		value = random.randint(0,255)
		row.append(value)
	print(row)
	return row

if __name__ == "__main__":
	while True:
		gen_row()

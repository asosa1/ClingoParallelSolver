import sys
def main():
	with open(sys.argv[1], 'r') as my_file:
		newline = my_file.read().replace('edge(1', 'edge(3')
		newline = newline.replace('vertice(1', 'vertice(3')

	with open("output.txt", "w") as output:
		output.write(newline)


if __name__ == "__main__":
	main()
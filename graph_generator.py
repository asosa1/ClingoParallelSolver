import random
def generate_graph(n):
	graph = [[-1 for i in range(n)] for j in range(n)]
	for i in range(n):
		for j in range(n):
			if j == i:
				graph[i][j] = 1
			if graph[i][j] == -1:
				temp = int(rando())		
				graph[i][j] = temp
				graph [j][i] = temp
	
	return graph


def rando(percentage = 33):
	return random.randrange(100) < percentage

def connected(graph, n):
	visited = [0 for i in range(n)]
	stack = []
	stack.append(graph[0][0])
	while stack:
		vertice = stack.pop()
		for i in range(n):
			if graph[vertice][i] == 1:
				if visited[i] == 0:
					visited[i] = 1
					stack.append(i)

	return 0 not in visited

def make_file(graph, filename, server, offset):
	file = open(filename, "w")
	for i in range(len(graph)):
		for j in range(len(graph)):
			if graph[i][j] == 1:
				if j == i:
					temp = offset + i
					line = "vertice(" + str(server) + ", " + str(temp) + ").\n"
					file.write(line)
				else:
					vertice1 = offset + i
					vertice2 = offset + j
					line = "edge(" + str(server) + ", " + str(vertice1) + ", " + str(vertice2) + ").\n" 
					file.write(line)

	file.close()



def main():
	temp = 0
	n = 100
	graph =[[0 for i in range(n)] for j in range(n)]
	while not temp:
		graph = generate_graph(n)
		temp = connected(graph, n)
	print graph

	make_file(graph, "test.txt", 0, 300)

if __name__ == "__main__":
	main()


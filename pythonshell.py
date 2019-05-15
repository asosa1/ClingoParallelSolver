#TODO: find way to pause processes when we one reaches a swap, look into changing input mid solution?? 
#support multiple groups of agents
#fix collision on second run
import subprocess
import string
import sys
import time


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.find( last, start )
        return s[start:end]
    except ValueError:
        return ""

#output: the output of the server we're using
#numagents: number of agents in the output
#server: the server number we're using
#returns a list of the updated agents, seperated by a space 
def updateagents(output, numagents, server, offset):
	newagents = ''
	for i in range(numagents):
		start = "move("
		start = (start + str(i + offset))	
		result = find_between_r(output, start, ")")

		if result: 
			a = result.rfind(',')
			b = result.rfind(',', 0, a)
			result = result[b+1:a]
			agent = "agent(" + str(i + offset) + ", " + server + ", " + result + ", a). " 
			newagents += agent + " "
		else:
			start = "agent(" + str(i + offset)
			result = find_between_r(output, start, ")")
			result = start + result + ")."
			newagents += result + " " 
	return newagents

def processswap(output):
	result = [None] * 2
	result[0] = "agent("
	start = "swap("
	processing = list(find_between(output, start, ")"))
	processed = [None] * 9
	if processing:

		#find first piece of info
		a = processing.index(',')
		temp = ''
		b = 0
		while(b < a):
			temp += processing[b]
			b +=1
		processed[0] = temp

		#find information between 2 commas
		a = processing.index(',')
		for i in range (0,7):
			temp = ''
			processing[a] = '.'
			b = processing.index(',')
			a +=1
			while(a < b):
				temp += processing[a]  
				a+=1
			processed[i + 1] = temp

		#find last piece of info
		a = processing.index(',') + 1
		temp = ''
		while(a < len(processing)):
			temp += processing[a]
			a += 1

		processed[len(processed)-1] = temp
		#return the processed swap at index 0, and the server the swap is going to in index 1
		result[0] += processed[2] + ", " + processed[1] + ", " + processed[5] + ", " + processed[4] + ")" + ". "
		result[0] += "goal(" + processed[0] + ", " + processed[1] + ", " +  processed[2] + ", " + processed[3] + ", " + "0, " + processed[7] + "). "
		result[1] = processed[6]
		return result


#output: the output of the server we're using
#returns the server number of the output
def findserver(output):
	start = "agent("
	server = find_between(output, start, ")")
	a = server.find(',')
	b = server.find(',', a+1)
	server = server[a+1:b]
	return server



def numagentsm(agentfile):
	total = 0
	with open(agentfile) as f:
		for line in f:
			finded = line.find("agent")
			while finded != -1:
				total += 1
				finded = line.find("agent", finded + 5)
	return total



#output: the output of the server we're using
#returns a string w/ swaps converted into agents and goals
def updateswap(output, agentlist, servers, i):
	index = output.find("swap(")
	solution = [''] * servers
	result = [None] * 2
	swap = ''
	while index != -1:
		swap_info = list(find_between(output, "swap(", ")"))
		prune_id = "agent(" + swap_info[4]
		prune_id = prune_id + find_between(agentlist, prune_id, ")") + ")."
		agentlist = agentlist.replace(prune_id, '')
		#turn our swap into an agent and a goal
		results = processswap(output)
		swap += results[0]
		solution[int(results[1])] += results[0]
		#remove the swap
		output = output[:index] + ' ' + output[index + 4:] 
		#move on to handling the next swap
		index = output.find("swap(")

	result[0] = swap
	result[1] = agentlist
	solution[i] = agentlist
	return solution


def main():
	
	start_time = time.time()

	#parameters
	agents = list()
	maps = list()
	with open(sys.argv[1], 'r') as my_file:
		line = my_file.readline() 
		agents = line.split()
		line = my_file.readline()
		maps = line.split()
	my_file.close()

	servers = len(maps)
	numagents = [None] * servers
	i = 0
	while i < servers:
		numagents[i] = numagentsm(agents[i])
		i += 1


	child_processes = []
	i = 0
	while i < servers:

		p1 = subprocess.Popen(["clingo", "iterative.lp", maps[i], agents[i]], stdout=subprocess.PIPE)
		child_processes.append(p1)
		i+=1


	for cp in child_processes:
		cp.wait()

	#format output of subprocesses so they can be input for next clingo run
	#removes all "fluff" from the output
	outputs = [None] * servers
	i = 0
	while i < servers:

		test = child_processes[i].communicate()[0]
		test1 = test.replace('Solving...', '').replace('clingo version 5.2.2', '').replace('Reading from iterative.lp ...', '').replace('Answer: 1', '').replace('SATISFIABLE', '')
		outputs[i] = test1.rsplit("\n", 5) [0]
		print(outputs[i])
		i +=1

	#process the swaps and properly move the agents and goals between servers
	results = [None] * servers
	i = 0
	offset = 0
	while i < servers:
		newagents = updateagents(outputs[i], int(numagents[i]), findserver(outputs[i]), offset)
		results[i] = updateswap(outputs[i], newagents, servers, i)
		offset = offset + numagents[i]
		i+=1
	
	#print results

	i = 0
	while i < servers:
		final = ''
		filename = str(i) + "-2.agents"
		file = open(filename, "w")
		final = final + results[i][i]
	
		j = 0
		while j < servers:
			if j == i:
				j+=1
				continue
			else:
				if results[j][i] is None:
					j+=1
					continue
				else: 
					final = final + results[j][i]
			j+=1
	
		i+=1
		file.write(final)
		file.close()

	child_processes = []
	i = 0

	while i < servers:
		filename = str(i) + "-2.agents"
		p1 = subprocess.Popen(["clingo", "iterative.lp", maps[i], filename], stdout=subprocess.PIPE)
		child_processes.append(p1)
		i+=1


	for cp in child_processes:
		cp.wait()

	i = 0 
	while i < servers:
		print(child_processes[i].communicate()[0])
		i+=1

	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
	main()









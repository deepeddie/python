

with open("C:\Projects\GitHub\python\wte\Personalization\Global_Subscribers.txt") as infile:
    for line in infile:
    	idx = line.find('\t')
    	if(idx != -1):
    		print line[:idx]
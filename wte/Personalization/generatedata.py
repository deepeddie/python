import csv
import random
import time

def assigninterests(mode) :
    allinterests = [90081, 90082, 90083];
    interest = random.choice(allinterests);
    #print('i = ' + str(interest))
    return [interest]

def assigntags(mode) :
    if(mode==90000) :
        allweeks = [90001, 90010, 90040];
        week = random.choice(allweeks);
        month = (week - 90000)/4 - 1;
        trimester = month / 3;
        #print('w = ' + str(week))
        #print('m = ' + str(month))
        #print('t = ' + str(trimester))
        return [week,month,trimester]
    
    if(mode==90060) :
        allyears = [90061, 90062, 90063];
        year = random.choice(allyears);
        #print('y = ' + str(year))
        return [year]

def processuser(userid):
    allmodes = [90000, 90060];
    mode = random.choice(allmodes)
    #print(mode)

    return [assigntags(mode), assigninterests(mode)];


#with open('tagids.csv') as csvfile:
    #reader = csv.DictReader(csvfile)
    #for row in reader:
        #print(row['tagid'], row['tagname'])

#with open('userids.txt') as csvfile:
    #reader = csv.DictReader(csvfile)
    #for row in reader:
        #print(row['userid']);
        #print(processuser(row['userid']));

start_time = time.time();

for i in range(1, 1000000):
    ruid = random.randrange(100000)
    #print()
    processuser(ruid);

print('time taken = %s seconds ' %(time.time() - start_time) )
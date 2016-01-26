import csv
import random
import time

def formatrecordrow(u, a,b='-'):
    return [u,a,b];

def assigninterests(cid) :
    retlist = list();
    if(not bool(g_keys)):
        return
    interests = random.sample(g_keys, 2);
    for interest in interests:
        retlist.append(formatrecordrow(cid, int(interest)));
    return retlist;

def assigntags(cid, mode) :
    retlist = list();
    smode = mode_tags[mode]['tagname'];
    #print(mode)
    if(smode=='Pregnancy') :
        week = 'w' + str(random.randrange(1,45,1));
        wtagid = w_tags[week]['wtagid']; 
        month = w_tags[week]['month'];
        mtagid = w_tags[week]['mtagid']; 
        trimester = w_tags[week]['trimester'];
        ttagid = w_tags[week]['ttagid']; 

        retlist.append(formatrecordrow(cid, int(ttagid), trimester));

        localrand = random.randrange(1,10,1);
        if( (localrand%3)==0 ):
            retlist.append(formatrecordrow(cid, int(mtagid), month));
        if( (localrand%5)==0 ):
            retlist.append(formatrecordrow(cid, int(mtagid), month));
            retlist.append(formatrecordrow(cid, int(wtagid), week));
    
    if(smode=='Baby') :
        if( not bool(b_keys)):
            return;
        year = random.choice(b_keys);
        retlist.append(formatrecordrow(cid, year));

    retlist.append(formatrecordrow(cid, mode));
    return retlist;

def processcontent(cid):
    if(not bool(mode_keys)):
        return

    retlist = list();

    if( (g_i % 4)==0 ):
        mode = random.choice(mode_keys)
    else:
        mode = '90000';
    # print(g_i)
    retlist = assigntags(cid, mode);
    retlist.extend(assigninterests(cid));
    # retlist.extend(assigninterests(userid));
    return retlist;
    #, assigninterests(mode)];

def readtagsasdict(filename):
    tags = {};
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['tagenabled'] == '1'):
                tags[row['tagid']] = row;
    return tags;

def readtags(filename):
    tags = list();
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags.append(row['tagid']);
    return tags;

def readpregnancytags(filename):
    tags = {};
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags[row['week']] = row;
    return tags;

mode_tags = {}
mode_tags = readtagsasdict('Tags-Modes.csv');
mode_keys = mode_tags.keys();
w_tags = {}
w_tags = readpregnancytags('Tags-Pregnancy.csv');
w_keys = w_tags.keys();
b_tags = {}
b_tags = readtagsasdict('Tags-Toddler.csv');
b_keys = b_tags.keys();
g_tags = {}
g_tags = readtagsasdict('Tags-Generic.csv');
g_keys = g_tags.keys();

#with open('userids.txt') as csvfile:
    #reader = csv.DictReader(csvfile)
    #for row in reader:
        #print(row['userid']);
        #print(processuser(row['userid']));


g_i = 1;
start_time = time.time();

# with open("output.csv", "wb") as f:
#     writer = csv.writer(f)
#     for i in range(1, 100):
#         ruid = random.randrange(100000);
#         ret = processuser(ruid);
#         # print(ret);
#         writer.writerows(ret)
#         g_i += 1;

# print('time taken = %s seconds ' %(time.time() - start_time) )
# exit();

with open("c2tags-output.csv", "wb") as f:
    writer = csv.writer(f)
    with open("C:\\Projects\\GitHub\\python\\wte\\Personalization\\allcontentids.csv") as infile:
        for cid in infile:
            ret = processcontent(int(cid.strip()));
            #print ret;
            writer.writerows(ret)
            g_i += 1;


print('time taken = %s seconds ' %(time.time() - start_time) )
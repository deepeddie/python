import csv
import random
import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime('%m/%d/%Y' , time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)

def formatrecordrow(u, a,b='-'):
    return [u,a,b];

def formathistoryrecordrow(u, a,b,c,d):
    return [u,a,b,c,d];

def assigninterests(userid) :
    retlist = list();
    if(not bool(g_keys)):
        return
    interests = random.sample(g_keys, 2);
    for interest in interests:
        retlist.append(formatrecordrow(userid, int(interest)));
    return retlist;

def assigntags(userid, mode) :
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
        
        retlist.append(formatrecordrow(userid, int(wtagid), week));
        retlist.append(formatrecordrow(userid, int(mtagid), month));
        retlist.append(formatrecordrow(userid, int(ttagid), trimester));
        return retlist;

        # return w_tags[week];
    
    if(smode=='Baby') :
        if( not bool(b_keys)):
            return;
        year = random.choice(b_keys);
        return [formatrecordrow(userid, year)]

    if(smode=='Pregnancy Loss') :
        return [formatrecordrow(userid, mode)]

def processuser(userid):

    retlist = list();

    localrand = random.randrange(1,10,1);

    selectedcids = random.sample(g_allcids, localrand);

    for eachcid in selectedcids:
        retlist.append(formathistoryrecordrow(userid, 
                                        randomDate("1/1/2015 12:00 PM", "1/1/2016 12:00 PM", random.random()),
                                        random.choice([3,4]),
                                        eachcid,
                                        random.choice([1,2])));

    return retlist;


def readtagsasdict(filename):
    tags = {};
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['tagenabled'] == '1'):
                tags[row['tagid']] = row;
    return tags;

def readaslist(filename):
    allcids = list();
    with open(filename) as cidfile:
        for cid in cidfile:
            allcids.append(int(cid.strip()));
    return allcids;

def readpregnancytags(filename):
    tags = {};
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags[row['week']] = row;
    return tags;


print randomDate("1/1/2015 12:00 PM", "1/1/2016 12:00 PM", random.random())


g_allcids = readaslist("C:\\Projects\\GitHub\\python\\wte\\Personalization\\allcontentids.csv");



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

with open("userhistory-output.csv", "wb") as f:
    writer = csv.writer(f)
    with open("C:\\Projects\\GitHub\\python\\wte\\Personalization\\allehuserids.csv") as infile:
        for userid in infile:
            ret = processuser(int(userid.strip()));
            # print ret;
            writer.writerows(ret)
#             g_i += 1;


print('time taken = %s seconds ' %(time.time() - start_time) )




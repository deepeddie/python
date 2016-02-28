import sys, getopt
import csv
import random
import time

def formatrecordrow(u, a,b='-'):
    return [u,a,b];

def assigninterests(userid, mode) :
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
    if(not bool(mode_keys)):
        return

    retlist = list();

    if( (g_i % 7)==0 ):
        mode = random.choice(mode_keys)
    else:
        mode = '90000';
    # print(g_i)
    retlist = assigntags(userid, mode);
    retlist.extend(assigninterests(userid, mode));
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

def usage():
  print('generatedata4ehuserids.py -i <inputfile> -r <refdir> -o <outputfile>')
  sys.exit(2)
  
def main(argv):
  inputfile = ''
  outputfile = ''
  refdir = ''
  if( len(argv) == 0):
    usage()
  try:
    opts, args = getopt.getopt(argv,"hi:o:r:",["ifile=","ofile=","refdir="])
  except getopt.GetoptError:
    usage()
  
  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-r", "--refdir"):
      refdir = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
  
  print('Input file is %s ' % inputfile)
  if(len(inputfile) == 0):
    usage()
  print('Output file is %s ' % outputfile)
  if(len(outputfile) == 0):
    usage()
  print('Ref Dir is %s ' % refdir)
  if(len(refdir) == 0):
    rdir = '.\\'

  start_time = time.time();

  global g_i
  g_i = 1;
  global mode_tags
  mode_tags = readtagsasdict(rdir + 'Tags-Modes.csv');
  global mode_keys
  mode_keys = mode_tags.keys();
  global w_tags
  w_tags = readpregnancytags(rdir + 'Tags-Pregnancy.csv');
  global w_keys
  w_keys = w_tags.keys();
  global b_tags
  b_tags = readtagsasdict(rdir + 'Tags-Toddler.csv');
  global b_keys
  b_keys = b_tags.keys();
  global g_tags
  g_tags = readtagsasdict(rdir + 'Tags-Generic.csv');
  global g_keys
  g_keys = g_tags.keys();

  with open(outputfile, "wb") as f:
      writer = csv.writer(f)
      #with open("C:\\Projects\\GitHub\\python\\wte\\Personalization\\allehuserids.csv") as infile:
      with open(inputfile) as infile:
          for userid in infile:
              ret = processuser(int(userid.strip()));
              writer.writerows(ret)
              g_i += 1;

  print('time taken = %s seconds ' %(time.time() - start_time) )

# with open("output.csv", "wb") as f:
#     writer = csv.writer(f)
#     for i in range(1, 100):
#         ruid = random.randrange(100000);
#         ret = processuser(ruid);
#         # print(ret);
#         writer.writerows(ret)
#         g_i += 1;

if __name__ == "__main__":
   main(sys.argv[1:])

import sys, getopt
import os
import csv
import random
import time
from datetime import timedelta, date, datetime
from multiprocessing import Pool, Array, Process
import mymodule

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

def processdate(onedate, cidfile, uidfile, outputfile):

  sDate = onedate.strftime("%m/%d/%Y")
  retlist = list();

  g_1_allcids = readaslist(cidfile);
  # g_1_allcids = list(mymodule.all_cids)

  g_1_alluids = readaslist(uidfile);
  # g_1_alluids = list(mymodule.all_uids)

  uidcount = random.randrange(1,len(g_1_alluids),1);
  selecteduids = random.sample(g_1_alluids, uidcount);

  for eachuid in selecteduids:
    vwcount = 0
    cidcount = random.randrange(1,5,1);
    selectedcids = random.sample(g_1_allcids, cidcount);
    for eachcid in selectedcids:
      vwcount = vwcount + 1
      # every 4th content gets a tap event
      if( (vwcount % 4)==0 ):
        retlist.append(formathistoryrecordrow(eachuid, sDate, 3, eachcid, 1));
        retlist.append(formathistoryrecordrow(eachuid, sDate, 4, eachcid, 1));
      else:
        retlist.append(formathistoryrecordrow(eachuid, sDate, 3, eachcid, 1));

  foldername = onedate.strftime("%m-%d-%Y")
  
  if not os.path.exists(foldername):
    os.makedirs(foldername)
  
  thisoutputfile = foldername + '/' + outputfile 
  with open(thisoutputfile, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(retlist)
  return True;
    

def readaslist(filename):
    allcids = list();
    with open(filename) as cidfile:
        for cid in cidfile:
            allcids.append(int(cid.strip()));
    return allcids;

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


    
def initProcess(all_uids, all_cids):
  mymodule.all_uids = all_uids
  mymodule.all_cids = all_cids
  
    
def usage():
  print('generatehistorybydates.py -c <cidfile> -u <uidfile> -d <#ofdays> -s <startdate(mm-dd-YYYY)> -o <outputfile> -r <refdir>')
  sys.exit(2)
  
def main(argv):
  cidfile = ''
  uidfile = ''
  ndays = 1
  outputfile = ''
  refdir = ''
  startdate = ''
  if( len(argv) == 0):
    usage()
  try:
    opts, args = getopt.getopt(argv,"hc:u:d:s:o:r:",["cfile=","ufile=","days=","startdate=","ofile=","refdir="])
  except getopt.GetoptError:
    usage()
  
  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt in ("-c", "--cfile"):
      cidfile = arg
    elif opt in ("-u", "--ufile"):
      uidfile = arg
    elif opt in ("-d", "--days"):
      ndays = int(arg)
    elif opt in ("-s", "--startdate"):
      startdate = arg
    elif opt in ("-r", "--refdir"):
      refdir = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
  
  print('Content file is %s ' % cidfile)
  if(len(cidfile) == 0):
    usage()

  print('User file is %s ' % uidfile)
  if(len(uidfile) == 0):
    usage()

  print('Output file is %s ' % outputfile)
  if(len(outputfile) == 0):
    usage()

  print('# of days of history %d ' % ndays)

  print('Start Date is %s ' % startdate)
  if(len(startdate) == 0):
    base = date.today()
  else:
    base = datetime.strptime(startdate, '%m-%d-%Y')

  print('Ref Dir is %s ' % refdir)
  if(len(refdir) == 0):
    rdir = '.\\'

  start_time = time.time();

  # base = date.today()
  date_list = [base - timedelta(days=x) for x in range(0, ndays)]

  print('.\n'.join(map(lambda x:(x.strftime("%m-%d-%Y")), date_list)))
  

  global g_allcids
  g_allcids = readaslist(cidfile);
  g_allcids_shared = Array('i',g_allcids, lock=False)

  global g_alluids
  g_alluids = readaslist(uidfile);
  g_alluids_shared = Array('i',g_alluids, lock=False)
  
  # for eachdate in date_list:
    # ret = processdate(eachdate.strftime("%m/%d/%Y"),cidfile,uidfile);

  retlist = {}
  pool = Pool(initializer=initProcess, initargs=(g_alluids_shared, g_allcids_shared,))
  
  for onedate in date_list:
    retlist[onedate] = pool.apply_async(processdate, (onedate, cidfile, uidfile, outputfile, ));
  
  for eachdate in retlist:
    ret = retlist[eachdate].get()
    
  print('time taken = %s seconds ' %(time.time() - start_time) )



if __name__ == "__main__":
   main(sys.argv[1:])

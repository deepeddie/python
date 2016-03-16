import sys, getopt
import os
import csv
import random
from math import ceil
import time
from datetime import timedelta, date



def readpregnancytags(filename):
    tags = {};
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags[row['week']] = row;
    return tags;


class TheDates:
  pass
  

def calc_week(due_date):

    today_date = date.today()
    concept_date = due_date - timedelta(weeks=38)
    date_4_calc = due_date - timedelta(weeks=40)
    
    allthedates = TheDates()
    
    allthedates.due_date = due_date
    allthedates.concept_date = concept_date
    allthedates.today_date = today_date

    allthedates.weeks_preg = int((today_date - date_4_calc).days/7)
    allthedates.weeks_days_preg = int((today_date - date_4_calc).days%7)
    allthedates.week_of_preg = int(ceil((today_date - date_4_calc).days/7))
    
    week2use = 'w'+str(allthedates.weeks_preg)
    wtagid = w_tags[week2use]['wtagid']; 
    month = w_tags[week2use]['month'];
    mtagid = w_tags[week2use]['mtagid']; 
    trimester = w_tags[week2use]['trimester'];
    ttagid = w_tags[week2use]['ttagid']; 

    allthedates.month_of_preg = month[1:]
    allthedates.trimester_of_preg = trimester[1:]

    return allthedates

def main():
    global w_tags
    w_tags = readpregnancytags('Tags-Pregnancy.csv');

    dd1 = date(2016, 6, 13)
    atd = calc_week(dd1)
    
    print('Today\'s Date : ' + str(atd.today_date))
    print('Due Date : ' + str(atd.due_date))
    print('Conception Date : ' + str(atd.concept_date))
    print('You are ' + str(atd.weeks_preg) + ' weeks and ' 
    + str(atd.weeks_days_preg) + ' days pregnant')
    print('You are ' + str(atd.month_of_preg) + ' months pregnant and in trimester ' 
    + str(atd.trimester_of_preg) + ' of pregnancy')

    print('You are in week ' + str(atd.week_of_preg) + ' of your pregnancy')
    print('You are in month ' + str(atd.month_of_preg) + ' of pregnancy and in trimester ' 
    + str(atd.trimester_of_preg) + ' of pregnancy')
    
  
main()


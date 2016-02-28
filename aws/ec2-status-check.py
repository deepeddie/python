#!/usr/bin/python
#
#

import boto3, sys
from boto3.session import Session
from datetime import datetime

# AWS_ACCESS_KEY_ID
AKID='AKIAJLYZRTT6VDRFCSBQ'
# AWS_SECRET_ACCESS_KEY
ASAK='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'
# Region string
REGION='us-east-1'

def lambda_handler(event, context):
    curr_ts = datetime.now()
    scurr_date = str(curr_ts.date())
    scurr_time = str(curr_ts.time().hour) + '-' + str(curr_ts.time().minute)
    scurr_key = scurr_date + '-' + scurr_time

    print(scurr_date)
    print(scurr_time)
    print(scurr_key)

    boto3.set_stream_logger('boto3')

    session = Session(aws_access_key_id=AKID,
                  aws_secret_access_key=ASAK,
                  region_name=REGION)

    sMsg = '--------------------------------' + '\r\n'
    ec2 = session.client('ec2')
    instances = ec2.describe_instances()
    allRs = instances['Reservations']
    for r in allRs:
      allIs = r['Instances']
      for i in allIs:
        sMsg = sMsg + 'InstanceId = ' + i['InstanceId'] + '\r\n'
        sMsg = sMsg + 'Status = ' + i['State']['Name'] + '\r\n'
        sMsg = sMsg + 'Last Launch Time = ' + i['LaunchTime'].strftime('%m/%d/%Y %H:%M') + '\r\n'
        sMsg = sMsg + 'InstanceType = ' + i['InstanceType'] + '\r\n'
        sMsg = sMsg + 'Tags = ' + ', '.join(d['Key'] + '=' + d['Value'] for d in i['Tags']) + '\r\n'
        sMsg = sMsg + 'KeyName = ' + i['KeyName'] + '\r\n'
      sMsg = sMsg + '\r\n'
    sMsg = sMsg + '--------------------------------' + '\r\n'
    print(sMsg)
    
    sns = session.client('sns')
    sns.publish(TargetArn='arn:aws:sns:us-east-1:709166686991:DCTopic',
                Message=sMsg, Subject='EC2-STATUS-CHECK @ '+ scurr_key )
    
    
lambda_handler(None, None)

# This script created a queue
#
# Author - Paul Doyle Aug 2015
#
#
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError


import sys
sys.path.append('/data')
from keys import access_key_id, secret_access_key
conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

rs = conn.get_all_queues()
for q in rs:
	print q.id

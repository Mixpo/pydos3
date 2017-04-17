#!/usr/bin/python

import sys
import os
import re
import json
import boto3
from botocore.exceptions import ClientError

action = sys.argv[1]
s3 = boto3.resource('s3')
s3_bucket = ''
s3_key = ''

config_filepath = os.environ['HOME'] + '/.pydos3'
if not os.path.isfile(config_filepath):
    print '~/.pydos3 file not configured.'
    exit(1)

config_file = open(config_filepath, 'r')
for line in config_file:
    key, value = line.split('=')
    if key == 'BUCKET':
        s3_bucket = value.strip()
    elif key == 'KEY_PREFIX':
        s3_key = value.strip() + '/{0}.json'

if s3_bucket == '':
    print 'BUCKET is not defined. Is ~/.pydos3 configured correctly?'
    exit(1)
if s3_key == '':
    print 'KEY_PREFIX is not defined. Is ~/.pydos3 configured correctly?'
    exit(1)


# Get the domain out of a URL
def domain_parse(url):
    return re.search(r'://(.+?)/', url).group(1)

if action == 'get':
    input_raw = sys.stdin.read().strip()
    domain = domain_parse(input_raw)
    key = s3_key.format(domain)
    try:
        obj = s3.Object(s3_bucket, key)
        obj.load()
        response = obj.get()
        data = response['Body'].read()
        print data
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # A no-op response from docker login when credentials don't exist yet
            print '{}'
        else:
            raise e
elif action == 'store':
    input_raw = sys.stdin.read().strip()
    data_json = json.loads(input_raw)
    # Lame way to extract domain from url
    domain = domain_parse(data_json['ServerURL'])
    key = s3_key.format(domain)
    # Store the provided credentials to bucket
    obj = s3.Object(s3_bucket, key)
    obj.put(Body=input_raw, ServerSideEncryption='AES256')
elif action == 'erase':
    input_raw = sys.stdin.read().strip()
    domain = domain_parse(input_raw)
    key = s3_key.format(domain)
    obj = s3.Object(s3_bucket, key)
    obj.delete()

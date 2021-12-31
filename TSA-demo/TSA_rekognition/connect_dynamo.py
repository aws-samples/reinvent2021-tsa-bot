from pprint import pprint
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = os.path.dirname(basepath.cwd())+'/TSA_mecha/.env'
load_dotenv(envars)

def get_tsaimage(name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.client('dynamodb',aws_access_key_id=os.getenv('AWS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_KEY'), region_name='us-east-1')
    
    try:
        #response = dynamodb.query(TableName='tsa-images',KeyConditionExpression='id = :id and Allowed=:allowed',
        #FilterExpression='contains(labels,:label)',ExpressionAttributeValues={':label': {'S' : 'nn'},':id': {'S' : name}})
        response = dynamodb.scan(TableName='tsa-images',
        FilterExpression='contains(labels,:label) and Allowed=:allowed ',ExpressionAttributeValues={":label": {"S" : name} ,":allowed" : {"BOOL" : False}})
        print("response is")
        print(response) 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        recordFnd = response.get('Items')
        print("item is ")
        print(recordFnd)
        if recordFnd is None:
         return ''
        else :
         return response['Items']
          

if __name__ == '__main__':
    tsaimage =  get_tsaimage('Bottle')
    if tsaimage:
        print("Get tsa image succeeded:")
        pprint(tsaimage, sort_dicts=False)

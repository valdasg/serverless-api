import json
from datetime import datetime
import boto3
import os
import uuid
import logging
import dynamo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
table_name = str(os.environ['DYNAMODB_TABLE'])

def create(event, context):
    logger.info(f'Incoming request is {event}')
    post_str = event['body']
    post = json.loads(post_str)
    current_timestamp = datetime.now().isoformat()
    post['createdAt'] = current_timestamp
    post['id'] = str(uuid.uuid4())

    res = dynamo.put_item(
        TableName = table_name,
        Item = dynamo.to_item(post)
    )

    return (
        {'statusCode': 201}
        if res['ResponseMetadata']['HTTPStatusCode'] == 200
        else {
            'statusCode': 500,
            'body': 'An error occured while creating post',
        }
    )

def get(event, context):
    print(':::::==>', event['pathParameters'])
    logger.info(f'Incoming request is: {event}')
    
    # set default error response
    
    response = {
        'statusCode': 500,
        'body': 'An error occured while getting post'
        }
    
    print(':::::==>', event)
    
    post_query = dynamodb.get_item(
        TableNane = table_name, Key = {'id': {'S': post_id}}
    )
    
    post_id = event['pathParameters']['postId']
    
    if 'Item' in post_query:
        post = post_query['item']
        logger.info(f'post is: {post}')
        response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'body': json.dumps(dynamo.to_dict(post))}
        }
    return response

def all(event, response):
    # set default error response
    response = {
        'statusCode': 500,
        'body': 'An error occured while getting all posts'
        }

    scan_result = dynamodb.scan(TableName = table_name)['Items']

    posts = [dynamo.to_dict(item) for item in scan_result]
    
    response = {
        'statusCode': 200,
        'body': json.dumps(posts)
    }
    
    return response

def update(event, response):
    logger.info(f'Incoming request is: {event}')
    
    post_id = event['pathParameters']['postId']
    
    # set default error response
    response = {
        'statusCode': 500,
        'body': f'An error occured while updatin post {post_id}'
        }
    
    post_str = event['body']
    
    post = json.dumps(post_str)
    
    res = dynamo.ipdate_item(
        TableName = table_name,
        Key = {
            'id': {'S': post_id}
        },
        UpdateExpression = 'set content=:c, author=:a, updateAt=:u',
        ExpressionAttributeValues = {
            ':c': dynamo.to_item(post['content']),
            ':a': dynamo.to_item(post['author']),
            ':u': dynamo.datetime.now().isoformat()
        },
        ReturnValues = 'UPDATED_NEW'
    )
    
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            'statusCode': 200
        }
    
    return response

def delete(event, response):
    logger.info(f'Incoming request is: {event}')
    
    post_id = event['pathParameters']['postId']
    
    # set default error response
    response = {
        'statusCode': 500,
        'body': f'An error occured while deletin post {post_id}'
        }
    
    res = dynamo.delete_item(
        TableName = table_name,
        Key = {
            'id': {'S': post_id}
        }
    )
    
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            'statusCode': 204
        }
        
    return response
    

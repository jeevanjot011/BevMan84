import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BevMan84-Orders')

sns = boto3.client('sns')
TOPIC_ARN = "arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:BevMan84-Notifications"

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        order = {
            'order_id': str(body['order_id']),
            'username': body['username'],
            'product': body['product'],
            'distance_km': str(body['distance']),
            'timestamp': datetime.utcnow().isoformat()
        }
        table.put_item(Item=order)

        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=f"New Order #{order['order_id']} from {order['username']}: {order['product']} ({order['distance_km']}km)",
            Subject="BevMan84 Order"
        )
    return {'statusCode': 200}
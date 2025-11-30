import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BevMan84-Orders')

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        order = {
            'order_id': str(body['order_id']),
            'username': body['username'],
            'product': body['product'],
            'area_code': body.get('area_code', 'unknown'),
            'delivery_date': str(body['delivery_date']),
            'distance_km': str(body['distance']),
            'transport': str(body['transport_suggestion']),
            'collect_message': body.get('collect_message', '')
        }

        table.put_item(Item=order)

       
    return {'statusCode': 200}
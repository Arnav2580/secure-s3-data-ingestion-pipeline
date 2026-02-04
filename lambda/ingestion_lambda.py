import json
import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "ProcessedRecords"

def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(response["Body"].read())

    table = dynamodb.Table(TABLE_NAME)

    for record in data:
        if "device_id" in record and "timestamp" in record and "value" in record:
            table.put_item(
                Item={
                    "device_id": record["device_id"],
                    "timestamp": record["timestamp"],
                    "value": record["value"]
                }
            )

    return {
        "statusCode": 200,
        "body": "Data processed securely"
    }

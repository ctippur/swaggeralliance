import boto3

class Insert(object):
   def __init__(self,table,object):
      ## For a Boto3 client ('client' is for low-level access to Dynamo service API)
      ddb1 = boto3.client('dynamodb',
        endpoint_url='http://localhost:8000',
        aws_access_key_id="anything",
        aws_secret_access_key="anything",
        region_name='us-west-2')
      response = ddb1.list_tables()
      print(response)
      
      # For a Boto3 service resource ('resource' is for higher-level, abstracted access to Dynamo)
      ddb2 = boto3.resource('dynamodb', endpoint_url='http://localhost:8000',
        aws_access_key_id="anything",
        aws_secret_access_key="anything",
        region_name='us-west-2')
      print(list(ddb2.tables.all()))

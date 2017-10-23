_author_ = 'ctippur'
import boto3
import os
from aws_requests_auth.aws_auth import AWSRequestsAuth

class credsaws():
    ## init
    session = boto3.session.Session()
    #es_host='search-enrichment-service-ebin6h6q5xc7ehx2snhwbtyl3m.us-west-2.es.amazonaws.com'
    #es_host=os.environ['es_endpoint']
    def __init__(self):
    	credentials=self.session.get_credentials().get_frozen_credentials()
    	self.awsauth = AWSRequestsAuth(
            	aws_access_key=credentials.access_key,
            	aws_secret_access_key=credentials.secret_key,
            	aws_token=credentials.token,
            	aws_host=self.es_host,
            	aws_region=self.session.region_name,
            	aws_service='es'
        	)

    def getAuth(self):
	       return self.awsauth

    def getESHost(self):
	       return self.es_host

class credslocal(object):
    ## init
    session = boto3.session.Session(
        region_name='us-east-1',
        aws_access_key_id='example_key_id',
        aws_secret_access_key='my_super_secret_key'
    )
    awsauth = None
    def __init__(self, service):
        print ("In init")
        print (boto3.__version__)
        self.session.resource(service)

        self.awsauth = AWSRequestsAuth(
            	aws_access_key="credentials.access_key",
            	aws_secret_access_key="credentials.secret_key",
            	aws_token="credentials.token",
            	aws_host="self.es_host",
            	aws_region="us-east-1",
                aws_service=service
        	)


    def getAuth(self):
        return self.awsauth

    def getSession(self):
        return self.session

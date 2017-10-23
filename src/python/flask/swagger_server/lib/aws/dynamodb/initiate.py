from flask import Flask
from flask_dynamo import Dynamo
import sys
import os
root=os.getcwd()
sys.path.append(root + '/swagger_server/lib/aws')
import Creds

class Initiate(object):
    app = Flask(__name__)
    def __init__(self, creds):
        app=self.app
        app.config['DYNAMO_TABLES'] = [
            {
                 "TableName":'patient',
                 "KeySchema":[dict(AttributeName='PatientID', KeyType='HASH'),dict(AttributeName='DeviceID', KeyType='SORT')],
                 "AttributeDefinitions":[dict(AttributeName='PatientID', AttributeType='S'),dict(AttributeName='DeviceID', AttributeType='S')],
                 "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
            }, {
                 "TableName":'groups',
                 "KeySchema":[dict(AttributeName='name', KeyType='HASH')],
                 "AttributeDefinitions":[dict(AttributeName='name', AttributeType='S')],
                 "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
            }, {
                 "TableName":'Test',
                 "KeySchema":[dict(AttributeName='TestID', KeyType='HASH')],
                 "AttributeDefinitions":[dict(AttributeName='TestID', AttributeType='S')],
                 "ProvisionedThroughput":dict(ReadCapacityUnits=10, WriteCapacityUnits=10)
            },{
                 "TableName":'users',
                 "KeySchema":[dict(AttributeName='username', KeyType='HASH')],
                 "AttributeDefinitions":[dict(AttributeName='username', AttributeType='S')],
                 "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
             }
        ]
        app.config['DYNAMO_SESSION'] = creds.getSession()

    def initiateLocal(self):
        app=self.app
        app.config['DYNAMO_ENABLE_LOCAL'] = True
        app.config['DYNAMO_LOCAL_HOST'] = 'localhost'
        app.config['DYNAMO_LOCAL_PORT'] = 8000
        dynamo = Dynamo(app)
        """
        with app.app_context():
            dynamo.create_all()
        """
        dynamo.init_app(app)
        return dynamo

    def initiateAws(self):
        app=self.app
        dynamo = Dynamo(app)
        return dynamo

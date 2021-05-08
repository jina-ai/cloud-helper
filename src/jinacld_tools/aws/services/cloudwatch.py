from pathlib import Path
from jinacld_tools.aws.logger import get_logger
from jinacld_tools.aws.client import AWSClientWrapper
from s3 import S3Bucket

import boto3

from dotenv import dotenv_values
config = dotenv_values("/Users/candice/Codes/jina/cloud-helper/.env")

accountID = config["ACCOUNT_ID"]
instanceID = config["INSTANCE_ID"]
ACCESS_KEY_ID = config["ACCESS_KEY_ID"]
SECRET_ACCESS_KEY = config["SECRET_ACCESS_KEY"]

class CloudWatch:
    """Wrapper around boto3 to fetch CloudWatch logs
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self._client_wrapper = AWSClientWrapper(service='cloudwatch')
        self._client = self._client_wrapper.client
        self.metrics = "" # url of metrics collected

    def fetch(self, ec2ARN):
        '''
            given an ec2 instance's ARN, e.g. "arn:aws:ec2:region:accountID:instanceID
            collect system metrics
            - AWS provided : CPU, Disk, Network data, status check(VM instance and its hardware)
            - custom : RAM
        '''
        _, _, _, region, _, instanceID = ec2ARN.split(":")
        #session = boto3.Session(profile_name="dev", region_name="us-east-1")
        '''
        ec2 = boto3.client('ec2', region_name="us-east-2", #aws_instance_id=
                           aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        for each in ec2.describe_instances()["Reservations"]:
            print(each)
              #list_bucket_metrics_configurations())'''

        ec2 = boto3.resource('ec2', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        for instance in ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values':[instanceID]}]):
            print(instance)
            print(instance.state)
            #print(instance.report_status())

        cloudwatch = boto3.resource('cloudwatch', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        #metric_filter = [{'Name': 'Namespace', 'Values':['AWS/EC2']}]
        for metric in cloudwatch.metrics.filter(Filters=[{'Name': 'Namespace', 'Values':['AWS/EC2']}]):
            print(metric)

    def store(self):
        # lambda call s3
        S3_DEFAULT_BUCKET = 'lambda-handlers-jina'
        s3 = S3Bucket(bucket_name=S3_DEFAULT_BUCKET)
        #s3.add(metrics, "metrics")


cloudwatcher = CloudWatch()
ec2ARN = "arn:aws:ec2:us-east-2:"+accountID+":"+instanceID
cloudwatcher.fetch(ec2ARN)
cloudwatcher.store()

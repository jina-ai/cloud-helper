from pathlib import Path
from datetime import datetime, timedelta
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

    def fetch(self, ec2ARN, endTime, metrics):
        '''
            given an ec2 instance's ARN, e.g. "arn:aws:ec2:region:accountID:instanceID
            collect system metrics from (launch time to user defined end time)
            - AWS provided : CPU, Disk, Network data, status check(VM instance and its hardware)
            - custom : RAM
        '''
        _, _, _, region, _, instanceID = ec2ARN.split(":")
        '''
        from boto3.ec2.connection import EC2Connection
        conn = EC2Connection(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        conn = EC2Connection()
        print(f'conn: {conn}')'''

        #session = boto3.Session(profile_name="dev", region_name="us-east-1")
        '''
        ec2 = boto3.client('ec2', region_name="us-east-2", #aws_instance_id=
                           aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        for each in ec2.describe_instances()["Reservations"]:
            print(each)
              #list_bucket_metrics_configurations())'''

        ec2 = boto3.resource('ec2', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        instance = ec2.Instance(instanceID)

        for instance in ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values':[instanceID]}]):
            print(instance)
            print(instance.state)
            #print(instance.report_status())

        metrics = {}

        '''
        metric_names = ['DiskReadOps', 'DiskWriteBytes', CPUUtilization]
        cloudwatch = boto3.resource('cloudwatch', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        for metric_name in metric_names:
            metrics[metric_name] = cloudwatch.metrics.filter(Namespace='AWS/EC2', MetricName=metric_name)
        print(metrics)'''

        cloudwatch = boto3.client('cloudwatch', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        responses = []

        for metric in metrics:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instanceID
                    },
                ],
                MetricName=metric,
                StartTime=instance.launch_time,
                EndTime=endTime,
                Period=3600, #seconds in one hour
                Statistics=[
                    'Maximum'
                ]
            )

            responses.append(response)

        return responses

    def store(self, metrics):
        import pickle
        serializedMetricsObject = pickle.dumps(metrics)
        # lambda call s3
        S3_DEFAULT_BUCKET = 'lambda-handlers-jina'
        #s3 = S3Bucket(bucket_name=S3_DEFAULT_BUCKET)
        #s3.add(metrics, "metrics")
        s3 = boto3.client('s3')
        s3.put_object(Bucket=S3_DEFAULT_BUCKET, Key='EC2Metrics', Body=serializedMetricsObject)

'''
cloudwatcher = CloudWatch()
ec2ARN = "arn:aws:ec2:us-east-2:"+accountID+":"+instanceID
endTime='2021-05-09T23:18:00'
metrics = ['DiskReadOps', 'DiskWriteBytes', 'CPUUtilization']
metricsCollected = cloudwatcher.fetch(ec2ARN, endTime, metrics)
cloudwatcher.store(metricsCollected)'''

from pathlib import Path
from datetime import datetime, timedelta
from jinacld_tools.aws.logger import get_logger
from jinacld_tools.aws.client import AWSClientWrapper
from ec2 import EC2

import boto3
import os

accountID = os.environ.get("ACCOUNT_ID")
instanceID = os.environ.get("INSTANCE_ID")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")

class CloudWatch:
    """Wrapper around boto3 to fetch CloudWatch logs
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self._client_wrapper = AWSClientWrapper(service='cloudwatch')
        self._client = self._client_wrapper.client

    def fetch(self, ec2_arn, end_time, metrics):
        '''
            given an ec2 instance's ARN, e.g. "arn:aws:ec2:region:accountID:instanceID
            collect system metrics from (launch time to user defined end time)
            - AWS provided : CPU, Disk, Network data, status check(VM instance and its hardware)
            - custom : RAM
        '''
        _, _, _, region, _, instance_id = ec2_arn.split(":")

        cloudwatch = boto3.client('cloudwatch', region_name=region,
                aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        responses = []
        ec2 = boto3.resource('ec2', region_name=region,
                             aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        instance = ec2.Instance(instanceID)

        for metric in metrics:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    },
                ],
                MetricName=metric,
                StartTime=instance.launch_time,
                EndTime=end_time,
                Period=3600, #seconds in one hour
                Statistics=[
                    'Maximum'
                ]
            )

            responses.append(response)

        return responses
from ..client import AWSClientWrapper
from ..logger import get_logger


class CloudWatch:
    """Wrapper around boto3 to fetch CloudWatch logs
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self._client_wrapper = AWSClientWrapper(service='cloudwatch')
        self._client = self._client_wrapper.client

    def fetch(self,ec2ARN):
        # to do : fetch cloudwatch metrics
        self.metrics = ""

    def store(self):
        # to do : store metrics with s3
        pass
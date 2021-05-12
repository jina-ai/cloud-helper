from jinacld_tools.aws.logger import get_logger
from jinacld_tools.aws.client import AWSClientWrapper

class EC2:
    def __init__(self, instance_id: str):
        self._client = AWSClientWrapper(service='ec2').client
        self._instance = instance_id
        self._logger = get_logger(self.__class__.__name__)
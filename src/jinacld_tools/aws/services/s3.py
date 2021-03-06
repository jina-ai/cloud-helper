import glob
from pathlib import Path

from jinacld_tools.aws.logger import get_logger
from jinacld_tools.aws.client import AWSClientWrapper


class S3Bucket:
    """Wrapper around boto3 to upload to/download from S3 bucket
    """

    def __init__(self, bucket_name: str):
        self._client = AWSClientWrapper(service='s3').client
        self._bucket = bucket_name
        self._logger = get_logger(self.__class__.__name__)

    def add(self, path: str, key: str):
        if not Path(path).exists():
            self._logger.error(f'Invalid path: {path}! Nothing to upload!')
            raise FileNotFoundError(path)
        try:
            self._logger.info(f'Uploading object from `{path}` to S3 bucket `{self._bucket}` key `{key}`')
            for filename in glob.iglob(str(path) + '**/**', recursive=True):
                if Path(filename).is_file():
                    self._client.upload_file(filename, self._bucket, f'{key}/{filename}')
        except Exception as exp:
            self._logger.error(f'Got following exception while uploading object to S3 \n{exp}')
            raise

    def get(self, key: str, local_path):
        try:
            self._logger.info(f'Downloading object from `{self._bucket}:{key}` to file: {local_path}')
            # for filename in glob.iglob(path + '**/**', recursive=True):
            self._client.download_file(self._bucket, key, local_path)
        except Exception as exp:
            self._logger.error(f'Got following exception while downloading object from S3 \n{exp}')
            raise

from aws_quota.utils import get_account_id, get_paginated_results
import enum
import typing

import boto3
from botocore.config import Config


class QuotaScope(enum.Enum):
    ACCOUNT = 0
    REGION = 1
    INSTANCE = 2


class QuotaCheck:
    key: str = None
    description: str = None
    scope: QuotaScope = None
    service_code: str = None
    quota_code: str = None
    warning_threshold: float = None
    error_threshold: float = None
    # retries are needed to handle rate limitting
    # https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html
    retry_attempts: int = 15

    def __init__(self, boto_session: boto3.Session) -> None:
        super().__init__()

        self.boto_session = boto_session
        self.sq_client = boto_session.client('service-quotas', config=Config(
            retries = {
                'max_attempts': self.retry_attempts,
                'mode': 'standard'
            }
        ))

    def __str__(self) -> str:
        return f'{self.key}{self.label_values}'

    def count_paginated_results(self, service: str, method: str, key: str, paginate_args: dict = {}) -> int:
        return len(get_paginated_results(self.boto_session, service, method, key, paginate_args))

    @property
    def label_values(self):
        label_values = {
            'quota': self.key,
            'account': get_account_id(self.boto_session)
        }

        if self.scope in (QuotaScope.REGION, QuotaScope.INSTANCE):
            label_values['region'] = self.boto_session.region_name

        if self.scope == QuotaScope.INSTANCE:
            label_values['instance'] = self.instance_id

        return label_values

    @property
    def maximum(self) -> int:
        try:
            return int(self.sq_client.get_service_quota(ServiceCode=self.service_code, QuotaCode=self.quota_code)['Quota']['Value'])
        except self.sq_client.exceptions.NoSuchResourceException:
            return int(self.sq_client.get_aws_default_service_quota(ServiceCode=self.service_code, QuotaCode=self.quota_code)['Quota']['Value'])

    @property
    def current(self) -> int:
        raise NotImplementedError


class InstanceQuotaCheck(QuotaCheck):
    scope = QuotaScope.INSTANCE
    instance_id: str = None

    def __init__(self, boto_session: boto3.Session, instance_id) -> None:
        super().__init__(boto_session)

        self.instance_id = instance_id

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        raise NotImplementedError

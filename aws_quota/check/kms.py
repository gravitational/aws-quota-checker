from aws_quota.exceptions import NotImplementedInFavourOfCloudWatch
from .quota_check import QuotaCheck, QuotaScope


class CryptographicOperationsRequestRate(QuotaCheck):
    key = "kms_cryptographic_operations_request_rate"
    description = "The number of active DDL queries. DDL queries include CREATE TABLE and ALTER TABLE ADD PARTITION queries."
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-3CE0BBA0'
    

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DDL" ]
        raise NotImplementedInFavourOfCloudWatch(self)


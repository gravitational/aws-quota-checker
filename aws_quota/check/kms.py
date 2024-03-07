from aws_quota.exceptions import NotImplementedInFavourOfCloudWatch
from .quota_check import QuotaCheck, QuotaScope


class CryptographicOperationsRequestRate(QuotaCheck):
    key = "kms_cryptographic_operations_request_rate"
    description = "Maximum requests for cryptographic operations with a symmetric CMK per second"
    scope = QuotaScope.REGION
    service_code = "kms"
    quota_code = "L-6E3AF000"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Class", "None", "Resource", "CryptographicOperationsSymmetric", "Service", "KMS", "Type", "API" ]
        raise NotImplementedInFavourOfCloudWatch(self)

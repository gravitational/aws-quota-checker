from aws_quota.exceptions import NotImplementedInFavourOfCloudWatch
from .quota_check import QuotaCheck, QuotaScope


class CryptographicOperationsRequestRate(QuotaCheck):
    key = "kms_cryptographic_operations_request_rate"
    scope = QuotaScope.REGION
    service_code = "kms"
    quota_code = "L-6E3AF000"
    description = "Maximum requests for cryptographic operations with a symmetric CMK per second. This shared quota applies to Decrypt, Encrypt, GenerateDataKey, GenerateDataKeyWithoutPlaintext, GenerateMac, GenerateRandom, ReEncrypt, and VerifyMac requests. When you reach this quota, KMS rejects this type of request for the remainder of the interval."

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Class", "None", "Resource", "CryptographicOperationsSymmetric", "Service", "KMS", "Type", "API" ]
        raise NotImplementedInFavourOfCloudWatch(self)

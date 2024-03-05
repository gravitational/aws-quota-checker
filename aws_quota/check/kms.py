from .quota_check import QuotaCheck, QuotaScope


class CryptographicOperationsRequestRate(QuotaCheck):
    key = "kms_cryptographic_operations_request_rate"
    description = "The number of active DDL queries. DDL queries include CREATE TABLE and ALTER TABLE ADD PARTITION queries."
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-3CE0BBA0'

    ## Current usage can be found in CloudWatch under:
    ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DDL" ]

class AthenaActiveDMLQueries(QuotaCheck):
    key = "athena_actvice_dml_queries_count"
    description = """
    Maximum requests for cryptographic operations with a symmetric CMK per second. 
    This shared quota applies to Decrypt, Encrypt, GenerateDataKey, GenerateDataKeyWithoutPlaintext, GenerateMac, GenerateRandom, ReEncrypt, and VerifyMac requests.
    When you reach this quota, KMS rejects this type of request for the remainder of the interval.
    """
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-6E3AF000'

    ## Current usage can be found in CloudWatch under:
    ## ["AWS/Usage", "CallCount", "Class", "None", "Resource", "CryptographicOperationsSymmetric", "Service", "KMS", "Type", "API"]

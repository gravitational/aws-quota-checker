from .quota_check import QuotaCheck, QuotaScope


class BucketCountCheck(QuotaCheck):
    key = "s3_bucket_count"
    scope = QuotaScope.ACCOUNT
    service_code = 's3'
    quota_code = 'L-DC2B2D3D'
    quota_region_override = 'us-east-1'
    description = "The number of Amazon S3 general purpose buckets that you can create in an account"

    @property
    def current(self):
        return len(self.boto_session.client('s3').list_buckets()['Buckets'])

from .quota_check import QuotaCheck, QuotaScope


class BucketCountCheck(QuotaCheck):
    key = "s3_bucket_count"
    description = "The number of Amazon S3 general purpose buckets that you can create in an account"
    scope = QuotaScope.REGION
    service_code = 's3'
    quota_code = 'L-DC2B2D3D'

    @property
    def current(self):
        # TODO figure out if this is regional or account level
        return len(self.boto_session.client('s3').list_buckets()['Buckets'])

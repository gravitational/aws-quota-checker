import boto3
from .quota_check import QuotaCheck, QuotaScope


class TopicCountCheck(QuotaCheck):
    key = "ses_daily_sends"
    scope = QuotaScope.REGION
    service_code = 'ses'
    quota_code = 'L-804C8AE8'
    description = "The maximum number of emails that you can send in a 24-hour period for this account in the current Region."

    @property
    def current(self):
        return self.boto_session.client('ses').get_send_quota()['SentLast24Hours']

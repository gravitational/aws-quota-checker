import cachetools
from aws_quota.exceptions import InstanceWithIdentifierNotFound
from aws_quota.utils import get_paginated_results
import typing
import boto3
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope


@cachetools.cached(cache=cachetools.TTLCache(maxsize=1, ttl=60))
def get_all_sns_topic_arns(session: boto3.Session) -> typing.List[str]:
    return [topic['TopicArn'] for topic in get_paginated_results(session, 'sns', 'list_topics', 'Topics')]

@cachetools.cached(cache=cachetools.TTLCache(maxsize=3000, ttl=60))
def get_topic_attributes(session: boto3.Session, topic_arn) -> typing.List[str]:
    return session.client('sns').get_topic_attributes(TopicArn=topic_arn)

class TopicCountCheck(QuotaCheck):
    key = "sns_topics_count"
    description = "SNS topics per Account"
    scope = QuotaScope.ACCOUNT
    service_code = 'sns'
    quota_code = 'L-61103206'

    @property
    def current(self):
        return len(get_all_sns_topic_arns(self.boto_session))

class PendingSubscriptionCountCheck(QuotaCheck):
    key = "sns_pending_subscriptions_count"
    description = "Pending SNS subscriptions per Account"
    scope = QuotaScope.ACCOUNT
    service_code = 'sns'
    quota_code = 'L-1A43D3DB'

    @property
    def current(self):
        all_topic_arns = get_all_sns_topic_arns(self.boto_session)
        pending_subs = 0

        for arn in all_topic_arns:
            pending_subs += int(get_topic_attributes(self.boto_session, arn)['Attributes']['SubscriptionsPending'])

        return pending_subs


class SubscriptionsPerTopicCheck(InstanceQuotaCheck):
    key = "sns_subscriptions_per_topic"
    description = "SNS subscriptions per topics"
    service_code = 'sns'
    quota_code = 'L-A4340BCD'
    instance_id = 'Topic ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return get_all_sns_topic_arns(session)

    @property
    def current(self):
        try:
            topic_attrs = get_topic_attributes(self.boto_session, self.instance_id)['Attributes']
        except self.boto_session.client('sns').exceptions.NotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e

        return int(topic_attrs['SubscriptionsConfirmed']) + int(topic_attrs['SubscriptionsPending'])

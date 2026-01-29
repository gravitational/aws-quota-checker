import cachetools
import typing

import boto3
from aws_quota.exceptions import InstanceWithIdentifierNotFound
from aws_quota.utils import get_paginated_results
from .quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope



@cachetools.cached(cache=cachetools.TTLCache(maxsize=3000, ttl=60))
def get_inference_profile_summaries(session: boto3.Session,
                                    type_equals: str | None = None) -> typing.List[dict]:
    paginate_args = {}
    if type_equals:
        paginate_args['typeEquals'] = type_equals

    return get_paginated_results(
        session,
        'bedrock',
        'list_inference_profiles',
        'inferenceProfileSummaries',
        paginate_args,
    )


def list_application_inference_profiles(session: boto3.Session) -> typing.List[dict]:
    return get_inference_profile_summaries(session, type_equals='APPLICATION')


@cachetools.cached(cache=cachetools.TTLCache(maxsize=200, ttl=60))
def inference_profile_summaries_by_identifier(session: boto3.Session) -> dict[str, dict]:
    summaries = get_inference_profile_summaries(session)
    by_identifier = {}

    for summary in summaries:
        if 'inferenceProfileId' in summary:
            by_identifier[summary['inferenceProfileId']] = summary
        if 'inferenceProfileArn' in summary:
            by_identifier[summary['inferenceProfileArn']] = summary

    return by_identifier


# Based on https://docs.aws.amazon.com/general/latest/gr/bedrock.html
class BedrockInferenceProfilesPerAccount(QuotaCheck):
    key = "bedrock_inference_profiles_per_account_count"
    scope = QuotaScope.REGION
    service_code = 'bedrock'
    quota_code = 'L-40EC9882'
    description = "The maximum number of inference profiles per account."

    @property
    def current(self):
        return len(list_application_inference_profiles(self.boto_session))


class BedrockEndpointsPerInferenceProfile(InstanceQuotaCheck):
    key = "bedrock_endpoints_per_inference_profile_count"
    service_code = 'bedrock'
    quota_limit_override = 5
    description = "The maximum number of endpoints per inference profile."
    instance_id = 'Inference profile ID or ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        summaries = list_application_inference_profiles(session)
        return [summary['inferenceProfileId'] for summary in summaries]

    @property
    def current(self):
        summaries = list_application_inference_profiles(self.boto_session)
        summary = None
        for candidate in summaries:
            if candidate.get('inferenceProfileId') == self.instance_id:
                summary = candidate
                break
            if candidate.get('inferenceProfileArn') == self.instance_id:
                summary = candidate
                break

        if summary is None:
            raise InstanceWithIdentifierNotFound(self)

        return len(summary.get('models', []))

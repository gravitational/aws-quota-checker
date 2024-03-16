from typing import List
from .quota_check import InstanceQuotaCheck, QuotaScope
from aws_quota.utils import get_paginated_results

import boto3
import cachetools


@cachetools.cached(cache=cachetools.TTLCache(maxsize=1, ttl=60))
def get_all_repositories(session: boto3.Session) -> List[str]:
    services = ['ecr']
    # ECR is available in all regions, but ecr-public is only available in us-east-1
    if session.region_name == 'us-east-1':
        services.append('ecr-public')

    return [
        repository['repositoryArn'] 
        for service in services
        for repository in get_paginated_results(session, service, 'describe_repositories', 'repositories')
    ]

@cachetools.cached(cache=cachetools.TTLCache(10000, 60))    # 10k = default number of max registries per account
def get_repository_images(session: boto3.Session, repository_arn: str) -> List[str]:
    arn_parts = repository_arn.split(':')
    service = arn_parts[2]
    repository_name = arn_parts[5].removeprefix("repository/")
    return get_paginated_results(session, service, "describe_images", "imageDetails", {'repositoryName': repository_name})

class ImagesPerRepository(InstanceQuotaCheck):
    key = "ecr_images_per_repository"
    scope = QuotaScope.INSTANCE
    service_code = 'ecr'
    quota_code = 'L-03A36CE1'
    description = "The maximum number of images per repository."
    instance_id = 'Repository ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> List[str]:
        return get_all_repositories(session)

    @property
    def current(self):
        return len(get_repository_images(self.boto_session, self.instance_id))

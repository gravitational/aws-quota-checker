import cachetools
from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing
import boto3

from aws_quota.utils import get_paginated_results
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_elbv2s(session: boto3.Session):
    return get_paginated_results(session, 'elbv2', 'describe_load_balancers', 'LoadBalancers')

def get_albs(session: boto3.Session):
    return list(filter(lambda lb: lb['Type'] == 'application', get_elbv2s(session)))

def get_nlbs(session: boto3.Session):
    return list(filter(lambda lb: lb['Type'] == 'network', get_elbv2s(session)))

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_classic_elbs(session: boto3.Session):
    return get_paginated_results(session, 'elb', 'describe_load_balancers', 'LoadBalancerDescriptions')


class ClassicLoadBalancerCountCheck(QuotaCheck):
    key = "elb_clb_count"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-E9E9831D'
    description = "The maximum number of Classic Load Balancers per Region"

    @property
    def current(self):
        return len(get_classic_elbs(self.boto_session))


class ListenerPerClassicLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_clb"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-1A491844'
    description = "The maximum number of listeners per Classic Load Balancer"
    instance_id = 'Load Balancer Name'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [ lb['LoadBalancerName'] for lb in get_classic_elbs(session)]

    @property
    def current(self):
        try:
            return len(
                self.boto_session.client('elb').describe_load_balancers(
                    LoadBalancerNames=[self.instance_id]
                )['LoadBalancerDescriptions'][0]['ListenerDescriptions']
            )
        except self.boto_session.client('elb').exceptions.AccessPointNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class NetworkLoadBalancerCountCheck(QuotaCheck):
    key = "elb_nlb_count"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-69A177A2'
    description = "The maximum number of Network Load Balancers per Region"

    @property
    def current(self):
        return len(get_nlbs(self.boto_session))


class ListenerPerNetworkLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_nlb"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-57A373D6'
    description = "The maximum number of listeners per Network Load Balancer"
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_nlbs(session)]

    @property
    def current(self):
        try:
            return self.count_paginated_results('elbv2', 'describe_listeners', 'Listeners', {'LoadBalancerArn': self.instance_id})
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class ApplicationLoadBalancerCountCheck(QuotaCheck):
    key = "elb_alb_count"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-53DA6B97'
    description = "The maximum number of Application Load Balancers per Region"

    @property
    def current(self):
        return len(get_albs(self.boto_session))


class ListenerPerApplicationLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_alb"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-B6DF7632'
    description = "The maximum number of listeners per Application Load Balancer"
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_albs(session)]

    @property
    def current(self) -> int:
        try:
            return self.count_paginated_results('elbv2', 'describe_listeners', 'Listeners', {'LoadBalancerArn': self.instance_id})
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class TargetGroupCountCheck(QuotaCheck):
    key = "elb_target_group_count"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-B22855CB'
    description = "The maximum number of target groups per Region"

    @property
    def current(self):
        return self.count_paginated_results('elbv2', 'describe_target_groups', 'TargetGroups')


class TargetGroupsPerApplicationLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_target_groups_per_alb"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-822D1B1B'
    description = "The maximum number of target groups per Application Load Balancer"
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_albs(session)]

    @property
    def current(self) -> int:
        try:
            return self.count_paginated_results('elbv2', 'describe_target_groups', 'TargetGroups', {'LoadBalancerArn': self.instance_id})
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e

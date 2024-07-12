from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing
import boto3
import cachetools
from .quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope


@cachetools.cached(cache=cachetools.TTLCache(1, 600))
def get_route53_account_limits(session: boto3.Session, limit_type: str):
    return session.client("route53").get_account_limit(Type=limit_type)


@cachetools.cached(cache=cachetools.TTLCache(1, 600))
def get_route53_hosted_zone_limits(session: boto3.Session, limit_type: str, hosted_zone_id: str):
    return session.client("route53").get_hosted_zone_limit(Type=limit_type, HostedZoneId=hosted_zone_id)


@cachetools.cached(cache=cachetools.TTLCache(1, 600))
def list_route53_hosted_zones(session: boto3.Session):
    return session.client("route53").list_hosted_zones()["HostedZones"]


class HostedZoneCountCheck(QuotaCheck):
    key = "route53_hosted_zone_count"
    description = "Route53 Hosted Zones per Account"
    scope = QuotaScope.ACCOUNT
    service_code = "route53"

    @property
    def maximum(self):
        return get_route53_account_limits(self.boto_session, "MAX_HOSTED_ZONES_BY_OWNER")["Limit"]["Value"]

    @property
    def current(self):
        return get_route53_account_limits(self.boto_session, "MAX_HOSTED_ZONES_BY_OWNER")["Count"]


class HealthCheckCountCheck(QuotaCheck):
    key = "route53_health_check_count"
    description = "Route53 Health Checks per Account"
    scope = QuotaScope.ACCOUNT
    service_code = "route53"

    @property
    def maximum(self):
        return get_route53_account_limits(self.boto_session, "MAX_HEALTH_CHECKS_BY_OWNER")["Limit"]["Value"]

    @property
    def current(self):
        return get_route53_account_limits(self.boto_session, "MAX_HEALTH_CHECKS_BY_OWNER")["Count"]


class ReusableDelegationSetCountCheck(QuotaCheck):
    key = "route53_reusable_delegation_set_count"
    description = "Route53 Reusable Delegation Sets per Account"
    scope = QuotaScope.ACCOUNT
    service_code = "route53"

    @property
    def maximum(self):
        return get_route53_account_limits(self.boto_session, "MAX_REUSABLE_DELEGATION_SETS_BY_OWNER")["Limit"]["Value"]

    @property
    def current(self):
        return get_route53_account_limits(self.boto_session, "MAX_REUSABLE_DELEGATION_SETS_BY_OWNER")["Count"]


class TrafficPolicyCountCheck(QuotaCheck):
    key = "route53_traffic_policy_count"
    description = "Route53 Traffic Policies per Account"
    scope = QuotaScope.ACCOUNT
    service_code = "route53"

    @property
    def maximum(self):
        return get_route53_account_limits(self.boto_session, "MAX_TRAFFIC_POLICIES_BY_OWNER")["Limit"]["Value"]

    @property
    def current(self):
        return get_route53_account_limits(self.boto_session, "MAX_TRAFFIC_POLICIES_BY_OWNER")["Count"]


class TrafficPolicyInstanceCountCheck(QuotaCheck):
    key = "route53_traffic_policy_instance_count"
    description = "Route53 Traffic Policy Instances per Account"
    scope = QuotaScope.ACCOUNT
    service_code = "route53"

    @property
    def maximum(self):
        return get_route53_account_limits(self.boto_session, "MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER")["Limit"]["Value"]

    @property
    def current(self):
        return get_route53_account_limits(self.boto_session, "MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER")["Count"]


class RecordsPerHostedZoneCheck(InstanceQuotaCheck):
    key = "route53_records_per_hosted_zone"
    description = "Records per Route53 Hosted Zone"
    instance_id = "Hosted Zone ID"
    service_code = "route53"

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [zone["Id"] for zone in list_route53_hosted_zones(session)]

    @property
    def maximum(self):
        try:
            return get_route53_hosted_zone_limits(self.boto_session, "MAX_RRSETS_BY_ZONE", self.instance_id)["Limit"]["Value"]
        except self.boto_session.client("route53").exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e

    @property
    def current(self):
        try:
            return get_route53_hosted_zone_limits(self.boto_session, "MAX_RRSETS_BY_ZONE", self.instance_id)["Count"]
        except self.boto_session.client("route53").exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e


class AssociatedVpcHostedZoneCheck(InstanceQuotaCheck):
    key = "route53_vpcs_per_hosted_zone"
    description = "Associated VPCs per Route53 Hosted Zone"
    instance_id = "Hosted Zone ID"
    service_code = "route53"

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [zone["Id"] for zone in list_route53_hosted_zones(session) if zone["Config"]["PrivateZone"]]

    @property
    def maximum(self):
        try:
            return get_route53_hosted_zone_limits(self.boto_session, "MAX_VPCS_ASSOCIATED_BY_ZONE", self.instance_id)["Limit"]["Value"]
        except self.boto_session.client("route53").exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e

    @property
    def current(self):
        try:
            return get_route53_hosted_zone_limits(self.boto_session, "MAX_VPCS_ASSOCIATED_BY_ZONE", self.instance_id)["Count"]
        except self.boto_session.client("route53").exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e

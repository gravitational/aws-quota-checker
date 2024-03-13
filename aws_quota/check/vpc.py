from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope
from aws_quota.exceptions import InstanceWithIdentifierNotFound
from aws_quota.utils import get_paginated_results
import boto3
import botocore.exceptions
import cachetools
import typing


def check_if_vpc_exists(session: boto3.Session, vpc_id: str) -> bool:
    client = session.client('ec2')
    try:
        client.describe_vpcs(VpcIds=[vpc_id])
    except botocore.exceptions.ClientError:
        return False
    return True


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_vpcs(session: boto3.Session) -> typing.List[dict]:
    return get_paginated_results(session, 'ec2', 'describe_vpcs', 'Vpcs')

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_subnets(session: boto3.Session) -> typing.List[dict]:
    return get_paginated_results(session, 'ec2', 'describe_subnets', 'Subnets')

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_nat_gateways(session: boto3.Session) -> typing.List[dict]:
    return get_paginated_results(session, 'ec2', 'describe_nat_gateways', 'NatGateways')

@cachetools.cached(cache=cachetools.TTLCache(10, 60))
def count_nat_gateways_by_az(session: boto3.Session, az_name: str) -> int:
    nat_count_by_az = {}
    subnet_id_to_az = {}

    for s in get_all_subnets(session):
        az = s['AvailabilityZone']
        nat_count_by_az[az] = 0
        subnet_id_to_az[s['SubnetId']] = az

    for nat in get_all_nat_gateways(session):
        subnet = nat['SubnetId']
        nat_count_by_az[subnet_id_to_az[subnet]] += 1

    return nat_count_by_az.get(az_name)

def get_vpc_by_id(session: boto3.Session, vpc_id: str) -> dict:
    try:
        return next(filter(lambda vpc: vpc_id == vpc['VpcId'], get_all_vpcs(session)))
    except StopIteration:
        raise KeyError

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_vpc_peering_connections(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_vpc_peering_connections(
        Filters=[
            {'Name': 'status-code', 'Values': ['active']},
        ]
    )['VpcPeeringConnections']

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_sgs(session: boto3.Session) -> typing.List[dict]:
    return get_paginated_results(session, 'ec2', 'describe_security_groups', 'SecurityGroups')


def get_sg_by_id(session: boto3.Session, sg_id: str) -> dict:
    try:
        return next(filter(lambda sg: sg_id == sg['GroupId'], get_all_sgs(session)))
    except StopIteration:
        raise KeyError


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_rts(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_route_tables()['RouteTables']


def get_rt_by_id(session: boto3.Session, rt_id: str) -> dict:
    try:
        return next(filter(lambda rt: rt_id == rt['RouteTableId'], get_all_rts(session)))
    except StopIteration:
        raise KeyError


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_network_acls(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_network_acls()['NetworkAcls']


class VpcCountCheck(QuotaCheck):
    key = "vpc_count"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-F678F1CE'
    description = "The maximum number of VPCs per Region. This quota is directly tied to the maximum number of internet gateways per Region."

    @property
    def current(self):
        return len(get_all_vpcs(self.boto_session))


class InternetGatewayCountCheck(QuotaCheck):
    key = "ig_count"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-A4707A72'
    description = "The maximum number of internet gateways per Region. This quota is directly tied to the maximum number of VPCs per Region. To increase this quota, increase the number of VPCs per Region."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_internet_gateways", "InternetGateways")

class VpcEndpointCountCheck(QuotaCheck):
    key = "vpc_endpoint"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-1B52E74A'
    description = "The maximum number of gateway VPC endpoints per Region. The maximum is 255 gateway endpoints per VPC."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_vpc_endpoints", "VpcEndpoints")

class NetworkInterfaceCountCheck(QuotaCheck):
    key = "ni_count"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-DF5E4CA3'
    description = "The maximum number of network interfaces per Region."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_network_interfaces", "NetworkInterfaces")


class SecurityGroupCountCheck(QuotaCheck):
    key = "sg_count"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-E79EC296'
    description = "The maximum number of VPC security groups per Region."

    @property
    def current(self):
        return len(get_all_sgs(self.boto_session))

class NatGatewayCountCheck(InstanceQuotaCheck):
    key = "nat_count"
    scope = QuotaScope.INSTANCE
    service_code = 'vpc'
    quota_code = 'L-FE5A380F'
    description = "The maximum number of NAT gateways per Availability Zone. This includes NAT gateways in the pending, active, or deleting state."
    instance_id = 'Availability Zone Name'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.Set[str]:
        return set(s['AvailabilityZone'] for s in get_all_subnets(session))

    @property
    def current(self):
        return count_nat_gateways_by_az(self.boto_session, self.instance_id)

class RulesPerSecurityGroupCheck(InstanceQuotaCheck):
    key = "vpc_rules_per_sg"
    service_code = 'vpc'
    quota_code = 'L-0EA8095F'
    description = "The maximum number of inbound or outbound rules per VPC security group (120 rules in total). This quota is enforced separately for IPv4 and IPv6 rules. A rule that references a security group or prefix list ID counts as one rule each for IPv4 and IPv6. This quota multiplied by the security groups per network interface quota cannot exceed 1000."
    instance_id = 'Security Group ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [sg['GroupId'] for sg in get_all_sgs(session)]

    @property
    def current(self):
        try:
            sg = get_sg_by_id(self.boto_session, self.instance_id)
            return len(sg['IpPermissions']) + len(sg['IpPermissionsEgress'])
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class RouteTablesPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_route_tables_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-589F43AA'
    description = "The maximum number of route tables per VPC. The main route table counts toward this quota."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self):
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_route_tables(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['RouteTables'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class RoutesPerRouteTableCheck(InstanceQuotaCheck):
    key = "vpc_routes_per_route_table"
    service_code = 'vpc'
    quota_code = 'L-93826ACB'
    description = "The maximum number of non-propagated routes per route table. This quota can be increased up to a maximum of 1000; however, network performance might be impacted. This quota is enforced separately for IPv4 and IPv6 routes."
    instance_id = 'Route Table ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [rt['RouteTableId'] for rt in get_all_rts(session)]

    @property
    def current(self):
        try:
            rt = get_rt_by_id(self.boto_session, self.instance_id)
            return len(rt['Routes'])
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class SubnetsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_subnets_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-407747CB'
    description = "The maximum number of subnets per VPC."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self):
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_subnets(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['Subnets'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class AclsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_acls_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-B4A6D682'
    description = "The maximum number of network ACLs per VPC."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_network_acls(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['NetworkAcls'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class RulesPerAclCheck(InstanceQuotaCheck):
    key = "vpc_rules_per_acl"
    service_code = 'vpc'
    quota_code = 'L-2AEEBF1A'
    description = "The maximum number of inbound rules or outbound rules per network ACL (a total of 40 rules). This includes both IPv4 and IPv6 rules, and the default deny rules. This quota can be increased up to a maximum of 40; however, network performance might be impacted."
    instance_id = 'Network ACL ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [acl['NetworkAclId'] for acl in get_all_network_acls(session)]

    @property
    def current(self) -> int:
        acls = get_all_network_acls(self.boto_session)
        if self.instance_id in [acl['NetworkAclId'] for acl in acls]:
            return len(next(filter(lambda acl: self.instance_id == acl['NetworkAclId'], acls))['Entries'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class Ipv4CidrBlocksPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_ipv4_cidr_blocks_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-83CA0A9D'
    description = "The maximum number of IPv4 CIDR blocks per VPC. The primary CIDR block and all secondary CIDR blocks count toward this quota. This quota can be increased up to a maximum of 50."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            return len(list(filter(lambda cbas: cbas['CidrBlockState']['State'] == 'associated', vpc['CidrBlockAssociationSet'])))
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class Ipv6CidrBlocksPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_ipv6_cidr_blocks_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-085A6257'
    description = "The maximum number of IPv6 CIDR blocks per VPC."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            if 'Ipv6CidrBlockAssociationSet' not in vpc:
                return 0

            return len(list(filter(lambda cbas: cbas['Ipv6CidrBlockState']['State'] == 'associated', vpc['Ipv6CidrBlockAssociationSet'])))
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)

class ActiveVpcPeeringConnectionsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_peering_connections_per_vpc"
    service_code = 'vpc'
    quota_code = 'L-7E9ECCDB'
    description = "The maximum number of active VPC peering connections per VPC. This quota can be increased up to a maximum of 125."
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        peering_connections_per_vpc = 0
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            vpc_peering_connections = get_vpc_peering_connections(self.boto_session)
            for peering_connection in vpc_peering_connections:
                for vpc_info in [peering_connection['AccepterVpcInfo'], peering_connection['RequesterVpcInfo']]:
                    if vpc_info['VpcId'] == vpc['VpcId'] and self.boto_session.region_name == vpc_info['Region']:
                        peering_connections_per_vpc += 1

            return peering_connections_per_vpc
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)

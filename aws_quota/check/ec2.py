from typing import List
from .quota_check import QuotaCheck, QuotaScope

import boto3
import cachetools


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_running_ec2_instances(session: boto3.Session):
    instances = []
    paginator = session.client('ec2').get_paginator('describe_instances')
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]

    for page in paginator.paginate(Filters=filters):
        for res in page['Reservations']:
            instances += res['Instances']

    return instances

def get_running_on_demand_ec2_instances(session: boto3.Session):
    return list(filter(lambda inst: 'SpotInstanceRequestId' not in inst, get_all_running_ec2_instances(session)))

def get_running_spot_ec2_instances(session: boto3.Session):
    return list(filter(lambda inst: 'SpotInstanceRequestId' in inst, get_all_running_ec2_instances(session)))

def count_vcpus_for_instance_types(instances, instance_types):
    vcpu_count = 0
    for inst in instances:
        if inst['InstanceType'].startswith(instance_types):
            vcpu_count += inst['CpuOptions']['CoreCount'] * inst['CpuOptions']['ThreadsPerCore']

    return vcpu_count


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_spot_requests(session: boto3.Session):
    return session.client('ec2').describe_spot_instance_requests()[
        'SpotInstanceRequests']


class OnDemandStandardInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_standard_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-1216C47A"
    description = "Maximum number of vCPUs assigned to the Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z'))


class OnDemandFInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_f_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-74FC7D96"
    description = "Maximum number of vCPUs assigned to the Running On-Demand F instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('f'))


class OnDemandGInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_g_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-DB2E81BA"
    description = "Maximum number of vCPUs assigned to the Running On-Demand G and VT instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('g'))


class OnDemandInfInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_inf_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-1945791B"
    description = "Maximum number of vCPUs assigned to the Running On-Demand Inf instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('inf'))


class OnDemandPInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_p_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-417A185B"
    description = "Maximum number of vCPUs assigned to the Running On-Demand P instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('p'))


class OnDemandXInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_x_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-7295265B"
    description = "Maximum number of vCPUs assigned to the Running On-Demand X instances."

    @property
    def current(self):
        instances = get_running_on_demand_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('x'))


class SpotStandardRequestCountCheck(QuotaCheck):
    key = "ec2_spot_standard_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-34B43A08"
    description = "The maximum number of vCPUs for all running or requested Standard (A, C, D, H, I, M, R, T, Z) Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z'))


class SpotFRequestCountCheck(QuotaCheck):
    key = "ec2_spot_f_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-88CF9481"
    description = "The maximum number of vCPUs for all running or requested F Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('f'))


class SpotGRequestCountCheck(QuotaCheck):
    key = "ec2_spot_g_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-3819A6DF"
    description = "The maximum number of vCPUs for all running or requested G and VT Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('g'))


class SpotInfRequestCountCheck(QuotaCheck):
    key = "ec2_spot_inf_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-B5D1601B"
    description = "The maximum number of vCPUs for all running or requested Inf Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('inf'))


class SpotPRequestCountCheck(QuotaCheck):
    key = "ec2_spot_p_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-7212CCBC"
    description = "The maximum number of vCPUs for all running or requested P4, P3 or P2 Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('p'))


class SpotXRequestCountCheck(QuotaCheck):
    key = "ec2_spot_x_count"
    scope = QuotaScope.REGION
    service_code = "ec2"
    quota_code = "L-E3A00192"
    description = "The maximum number of vCPUs for all running or requested X Spot Instances per Region"

    @property
    def current(self):
        instances = get_running_spot_ec2_instances(self.boto_session)
        return count_vcpus_for_instance_types(instances, ('x'))


class ElasticIpCountCheck(QuotaCheck):
    key = "ec2_eip_count"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-0263D0A3'
    description = "The maximum number of Elastic IP addresses that you can allocate for EC2-VPC in this Region."

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_addresses()['Addresses'])


class TransitGatewayCountCheck(QuotaCheck):
    key = "ec2_tgw_count"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-A2478D36'
    description = "Number of transit gateways per Region per account."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_transit_gateways", "TransitGateways")


class VpnConnectionCountCheck(QuotaCheck):
    key = "ec2_vpn_connection_count"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-3E6EC3A3'
    description = "The maximum number of Site-to-Site VPN connections that you can create per region."

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_vpn_connections()['VpnConnections'])

class LaunchTemplatesCount(QuotaCheck):
    key = "launch_templates_count"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-FB451C26'
    description = "Maximum number of launch templates per Region per account."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_launch_templates", "LaunchTemplates")
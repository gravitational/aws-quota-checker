import typing
import boto3
import cachetools
from aws_quota.check.ec2 import get_all_running_ec2_instances

from aws_quota.utils import get_paginated_results
from .quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_eks_clusters(session: boto3.Session) -> typing.List[str]:
    return get_paginated_results(session, "eks", "list_clusters", "clusters")


@cachetools.cached(cache=cachetools.TTLCache(100, 60))
def get_node_groups(session: boto3.Session, cluster_name) -> typing.List[str]:
    return get_paginated_results(session, "eks", "list_nodegroups", "nodegroups", {'clusterName': cluster_name})

class ClusterCountCheck(QuotaCheck):
    key = "eks_count"
    description = "EKS Clusters per Region"
    scope = QuotaScope.REGION
    service_code = 'eks'
    quota_code = 'L-1194D53C'

    @property
    def current(self):
        return len(get_all_eks_clusters(self.boto_session))


class NodeGroupsPerCluster(InstanceQuotaCheck):
    key = "eks_node_groups_per_cluster_count"
    description = "The maximum number of managed node groups per cluster."
    service_code = 'eks'
    quota_code = 'L-6D54EA21'
    instance_id = 'Cluster ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return get_all_eks_clusters(session)

    @property
    def current(self):
        return len(get_node_groups(self.boto_session, self.instance_id))
    

class NodesPerNodeGroup(InstanceQuotaCheck):
    key = "eks_nodes_per_node_group_count"
    description = "The maximum number of nodes per managed node group"
    service_code = 'eks'
    quota_code = 'L-BD136A63'
    instance_id = {'eks_cluster': None, 'eks_nodegroup': None }

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        res = []
        for cluster in get_all_eks_clusters(session):
            for nodegroup in get_node_groups(session, cluster):
                res.append({'eks_cluster': cluster, 'eks_nodegroup': nodegroup })
        return res
    
    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)
        count = 0

        for inst in instances:
            eks_nodegroup_match = False
            eks_cluster_match = False
            for tag in inst['Tags']:
                if tag['Key'] == 'eks:nodegroup-name':
                    if tag['Value'] != self.instance_id['eks_nodegroup']:
                        continue
                    eks_nodegroup_match = True
                elif tag['Key'] == 'eks:cluster-name':
                    if tag['Value'] != self.instance_id['eks_cluster']:
                        continue
                    eks_cluster_match = True

            if eks_nodegroup_match and eks_cluster_match:
                count += 1

        return count

from .quota_check import QuotaCheck, QuotaScope


class ClusterCountCheck(QuotaCheck):
    key = "eks_count"
    description = "EKS Clusters per Region"
    scope = QuotaScope.REGION
    service_code = 'eks'
    quota_code = 'L-1194D53C'

    @property
    def current(self):
        return self.count_paginated_results("eks", "list_clusters", "clusters")

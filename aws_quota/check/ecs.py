from .quota_check import QuotaCheck, QuotaScope


class ClusterCountCheck(QuotaCheck):
    key = "ecs_count"
    scope = QuotaScope.REGION
    service_code = 'ecs'
    quota_code = 'L-21C621EB'
    description = "Number of clusters per account"

    @property
    def current(self):
        return self.count_paginated_results("ecs", "list_clusters", "clusterArns")

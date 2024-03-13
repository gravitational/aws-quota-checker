from .quota_check import QuotaCheck, QuotaScope


class SnapshotCountCheck(QuotaCheck):
    key = "ebs_snapshot_count"
    scope = QuotaScope.REGION
    service_code = 'ebs'
    quota_code = 'L-309BACF6'
    description = "The maximum number of snapshots per Region."

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_snapshots", "Snapshots", {"OwnerIds": ["self"]})

from .quota_check import QuotaCheck, QuotaScope


class RDSDBInstanceCountCheck(QuotaCheck):
    key = "rds_instances"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-7B6409FD"
    description = "The maximum number of DB instances allowed in this account in the current Region"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_instances", "DBInstances"
        )


class RDSDBParameterGroupsCountCheck(QuotaCheck):
    key = "rds_parameter_groups"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-DE55804A"
    description = "The maximum number of parameter groups"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_parameter_groups", "DBParameterGroups"
        )


class RDSDBClusterParameterGroupCountCheck(QuotaCheck):
    key = "rds_cluster_parameter_groups"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-E4C808A8"
    description = "The maximum number of DB cluster parameter groups"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_cluster_parameter_groups", "DBClusterParameterGroups"
        )


class RDSEventSubscriptions(QuotaCheck):
    key = "rds_event_subscriptions"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-A59F4C87"
    description = "The maximum number of event subscriptions"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_event_subscriptions", "EventSubscriptionsList"
        )


class RDSDBSnapshotsCheck(QuotaCheck):
    key = "rds_instance_snapshots"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-272F1212"
    description = "The maximum number of manual DB instance snapshots"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_snapshots", "DBSnapshots", {"SnapshotType": "manual"}
        )


class RDSDBClusterSnapshotsCheck(QuotaCheck):
    key = "rds_cluster_snapshots"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-9B510759"
    description = "The maximum number of manual DB cluster snapshots"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_cluster_snapshots", "DBClusterSnapshots", {"SnapshotType": "manual"}
        )

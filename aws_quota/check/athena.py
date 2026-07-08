from aws_quota.exceptions import NotImplementedInFavourOfCloudWatch
from .quota_check import QuotaCheck, QuotaScope


class AthenaActiveDDLQueries(QuotaCheck):
    key = "athena_active_ddl_queries_count"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-3CE0BBA0'
    description = "The number of active DDL queries. DDL queries include CREATE TABLE and ALTER TABLE ADD PARTITION queries."

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DDL" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaActiveDMLQueries(QuotaCheck):
    key = "athena_active_dml_queries_count"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-FC5F6546'
    description = "The number of active DML queries. DML queries include SELECT, CREATE TABLE AS (CTAS), and INSERT INTO queries. The specific quotas vary by AWS Region."

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DML" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaBatchGetNamedQueryReplenishmentRate(QuotaCheck):
    key = "athena_batch_get_named_query_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-076245C0'
    description = "Maximum call rate per second for BatchGetNamedQuery API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "BatchGetNamedQuery", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaBatchGetQueryExecutionReplenishmentRate(QuotaCheck):
    key = "athena_batch_get_query_execution_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-52EFA794'
    description = "Maximum call rate per second for BatchGetQueryExecution API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "BatchGetQueryExecution", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaCreateNamedQueryReplenishmentRate(QuotaCheck):
    key = "athena_create_named_query_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-76AFE6F2'
    description = "Maximum call rate per second for CreateNamedQuery API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "CreateNamedQuery", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaDeleteNamedQueryReplenishmentRate(QuotaCheck):
    key = "athena_delete_named_query_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-41075247'
    description = "Maximum call rate per second for DeleteNamedQuery API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "DeleteNamedQuery", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaGetNamedQueryReplenishmentRate(QuotaCheck):
    key = "athena_get_named_query_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-D0D8C912'
    description = "Maximum call rate per second for GetNamedQuery API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "GetNamedQuery", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaGetQueryExecutionReplenishmentRate(QuotaCheck):
    key = "athena_get_query_execution_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-9D86AA19'
    description = "Maximum call rate per second for GetQueryExecution API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "GetQueryExecution", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaGetQueryResultsReplenishmentRate(QuotaCheck):
    key = "athena_get_query_results_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-07F4444F'
    description = "Maximum call rate per second for GetQueryResults API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "GetQueryResults", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaListNamedQueriesReplenishmentRate(QuotaCheck):
    key = "athena_list_named_queries_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-82E47245'
    description = "Maximum call rate per second for ListNamedQueries API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "ListNamedQueries", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaListQueryExecutionsReplenishmentRate(QuotaCheck):
    key = "athena_list_query_executions_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-70FD91F7'
    description = "Maximum call rate per second for ListQueryExecutions API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "ListQueryExecutions", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaStartQueryExecutionReplenishmentRate(QuotaCheck):
    key = "athena_start_query_execution_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-4FF11DD3'
    description = "Maximum call rate per second for StartQueryExecution API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "StartQueryExecution", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

class AthenaStopQueryExecutionReplenishmentRate(QuotaCheck):
    key = "athena_stop_query_execution_replenishment_rate"
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-EFB619E3'
    description = "Maximum call rate per second for StopQueryExecution API in this account in the current Region. For this API, the service adds tokens to your account at a fixed rate. One token allows you to make one API call. You accumulate tokens for an API up to a maximum of (Replenishment rate quota of the API * Burst multiplier quota of the API)"

    @property
    def current(self):
        ## Current usage can be found in CloudWatch under:
        ## [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "StopQueryExecution", "Service", "Athena", "Class", "None" ]
        raise NotImplementedInFavourOfCloudWatch(self)

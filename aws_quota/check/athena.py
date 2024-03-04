from .quota_check import QuotaCheck, QuotaScope


class AthenaActiveDDLQueries(QuotaCheck):
    key = "athena_actvice_ddl_queries_count"
    description = "The number of active DDL queries. DDL queries include CREATE TABLE and ALTER TABLE ADD PARTITION queries."
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-3CE0BBA0'

    ## Current usage can be found in CloudWatch under:
    ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DDL" ]


class AthenaActiveDMLQueries(QuotaCheck):
    key = "athena_actvice_dml_queries_count"
    description = "The number of active DML queries. DML queries include SELECT, CREATE TABLE AS (CTAS), and INSERT INTO queries. The specific quotas vary by AWS Region."
    scope = QuotaScope.REGION
    service_code = 'athena'
    quota_code = 'L-FC5F6546'

    ## Current usage can be found in CloudWatch under:
    ## [ "AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "ActiveQueryCount", "Service", "Athena", "Class", "DML" ]

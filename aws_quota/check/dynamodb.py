from .quota_check import QuotaCheck, QuotaScope


class TableCountCheck(QuotaCheck):
    key = "dyndb_table_count"
    scope = QuotaScope.REGION
    service_code = 'dynamodb'
    quota_code = 'L-F98FE922'
    description = "The maximum number of tables that can be created per region. For more information, see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html#limits-tables"

    @property
    def current(self):
        return self.count_paginated_results("dynamodb", "list_tables", "TableNames" )

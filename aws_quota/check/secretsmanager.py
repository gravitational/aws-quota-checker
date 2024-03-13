from .quota_check import QuotaCheck, QuotaScope


class SecretCountCheck(QuotaCheck):
    key = "secretsmanager_secrets_count"
    description = "Secrets per Account"
    scope = QuotaScope.REGION
    service_code = 'secretsmanager'
    quota_code = 'L-2F66C23C'

    @property
    def current(self):
        return self.count_paginated_results("secretsmanager", "list_secrets", "SecretList" )

from .quota_check import QuotaCheck, QuotaScope


class SecretCountCheck(QuotaCheck):
    key = "secretsmanager_secrets_count"
    scope = QuotaScope.ACCOUNT
    service_code = 'secretsmanager'
    quota_code = 'L-2F66C23C'
    description = "The maximum number of secrets in each AWS Region of this AWS account."

    @property
    def current(self):
        return self.count_paginated_results("secretsmanager", "list_secrets", "SecretList" )

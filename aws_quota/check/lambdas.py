from .quota_check import QuotaCheck, QuotaScope


class FunctionAndLayerStorageCheck(QuotaCheck):
    key = "lambda_function_storage"
    scope = QuotaScope.REGION
    service_code = 'lambda'
    quota_code = 'L-2ACBD22F'
    description = "The amount of storage that's available for deployment packages and layer archives in the current Region."

    @property
    def current(self):
        return (
            self.boto_session.client('lambda').get_account_settings()['AccountUsage'][
                'TotalCodeSize'
            ]
            / 1000000000
        )

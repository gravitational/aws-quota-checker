from .quota_check import QuotaCheck, QuotaScope


class ApplicationCountCheck(QuotaCheck):
    key = "elasticbeanstalk_application_count"
    scope = QuotaScope.ACCOUNT
    service_code = 'elasticbeanstalk'
    quota_code = 'L-1CEABD17'
    description = "The maximum number of applications that you can create in this account in the current Region."

    @property
    def current(self):
        return len(self.boto_session.client('elasticbeanstalk').describe_applications()['Applications'])


class EnvironmentCountCheck(QuotaCheck):
    key = "elasticbeanstalk_environment_count"
    scope = QuotaScope.ACCOUNT
    service_code = 'elasticbeanstalk'
    quota_code = 'L-8EFC1C51'
    description = "The maximum number of environments that you can create in this account in the current Region. The limit applies across applications, not per application."

    @property
    def current(self):
        return len(self.boto_session.client('elasticbeanstalk').describe_environments()['Environments'])

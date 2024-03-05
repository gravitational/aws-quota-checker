class AwsQuotaCheckerException(RuntimeError):
    pass


class InstanceWithIdentifierNotFound(AwsQuotaCheckerException):
    def __init__(self, check) -> None:
        self.check = check

    def __str__(self) -> str:
        return f'check {self.check.key} could not find instance with ID "{self.check.instance_id}"'


class NotImplementedInFavourOfCloudWatch(AwsQuotaCheckerException):
    def __init__(self, check) -> None:
        self.check = check

    def __str__(self) -> str:
        return f'check {self.check.key} is not implemented, because CloudWatch metric is available'
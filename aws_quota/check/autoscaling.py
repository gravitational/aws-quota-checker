from .quota_check import QuotaCheck, QuotaScope


class AutoScalingGroupCountCheck(QuotaCheck):
    key = "asg_count"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-CDE20ADC'
    description = "The maximum number of Auto Scaling groups allowed for your AWS account"

    @property
    def current(self):
        return self.count_paginated_results("autoscaling", "describe_auto_scaling_groups", "AutoScalingGroups")


class LaunchConfigurationCountCheck(QuotaCheck):
    key = "lc_count"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-6B80B8FA'
    description = "The maximum number of launch configurations allowed for your AWS account"

    @property
    def current(self):
        return self.count_paginated_results("autoscaling", "describe_launch_configurations", "LaunchConfigurations")

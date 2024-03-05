from .quota_check import QuotaCheck, QuotaScope


class AutoScalingGroupCountCheck(QuotaCheck):
    key = "asg_count"
    description = "Auto Scaling groups per Region"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-CDE20ADC'

    @property
    def current(self):
        return self.count_paginated_results("autoscaling", "describe_auto_scaling_groups", "AutoScalingGroups")


class LaunchConfigurationCountCheck(QuotaCheck):
    key = "lc_count"
    description = "Launch configurations per Region"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-6B80B8FA'

    @property
    def current(self):
        return self.count_paginated_results("autoscaling", "describe_launch_configurations", "LaunchConfigurations")

import cachetools
from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing

import boto3
from .quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def iam_account_summary(session: boto3.Session):
    return session.client('iam').get_account_summary()

class GroupCountCheck(QuotaCheck):
    key = "iam_group_count"
    description = "IAM groups per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['GroupsQuota']

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['Groups']


class UsersCountCheck(QuotaCheck):
    key = "iam_user_count"
    description = "IAM users per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['UsersQuota']

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['Users']


class PolicyCountCheck(QuotaCheck):
    key = "iam_policy_count"
    description = "IAM policies per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['PoliciesQuota']

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['Policies']


class PolicyVersionCountCheck(QuotaCheck):
    key = "iam_policy_version_count"
    description = "IAM policy versions in use per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['PolicyVersionsInUseQuota']

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['PolicyVersionsInUse']


class ServerCertificateCountCheck(QuotaCheck):
    key = "iam_server_certificate_count"
    description = "IAM server certificates per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['ServerCertificatesQuota']

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['ServerCertificates']


class AttachedPolicyPerUserCheck(InstanceQuotaCheck):
    key = "iam_attached_policy_per_user"
    description = "Attached IAM policies per user"
    instance_id = "User Name"

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [user['UserName'] for user in session.client('iam').list_users()['Users']]

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['AttachedPoliciesPerUserQuota']

    @property
    def current(self):
        try:
            return len(self.boto_session.client('iam').list_user_policies(UserName=self.instance_id)['PolicyNames'])
        except self.boto_session.client('iam').exceptions.NoSuchEntityException as e:
            raise InstanceWithIdentifierNotFound(self) from e

class AttachedPolicyPerGroupCheck(InstanceQuotaCheck):
    key = "iam_attached_policy_per_group"
    description = "Attached IAM policies per group"
    instance_id = "Group Name"

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [user['GroupName'] for user in session.client('iam').list_groups()['Groups']]

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['AttachedPoliciesPerGroupQuota']

    @property
    def current(self):
        try:
            return len(self.boto_session.client('iam').list_group_policies(GroupName=self.instance_id)['PolicyNames'])
        except self.boto_session.client('iam').exceptions.NoSuchEntityException as e:
            raise InstanceWithIdentifierNotFound(self) from e

class AttachedPolicyPerRoleCheck(InstanceQuotaCheck):
    key = "iam_attached_policy_per_role"
    description = "Attached IAM policies per role"
    instance_id = "Role Name"

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [user['RoleName'] for user in session.client('iam').list_roles()['Roles']]

    @property
    def maximum(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['AttachedPoliciesPerRoleQuota']

    @property
    def current(self):
        try:
            return len(self.boto_session.client('iam').list_role_policies(RoleName=self.instance_id)['PolicyNames'])
        except self.boto_session.client('iam').exceptions.NoSuchEntityException as e:
            raise InstanceWithIdentifierNotFound(self) from e

class RoleCountCheck(QuotaCheck):
    key = "iam_role_count"
    description = "IAM roles per Account"
    scope = QuotaScope.ACCOUNT
    service_code = 'iam'
    quota_code = 'L-FE177D64'

    @property
    def current(self):
        return iam_account_summary(self.boto_session)['SummaryMap']['Roles']

    @property
    def maximum(self) -> int:
        return iam_account_summary(self.boto_session)['SummaryMap']['RolesQuota']

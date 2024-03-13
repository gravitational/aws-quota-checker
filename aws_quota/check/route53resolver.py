from .quota_check import QuotaCheck, QuotaScope


class EndpointCountCheck(QuotaCheck):
    key = "route53resolver_endpoint_count"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-4A669CC0'
    description = "Resolver endpoints per AWS Region"

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_endpoints()['ResolverEndpoints'])

class RulesCountCheck(QuotaCheck):
    key = "route53resolver_rule_count"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-51D8A1FB'
    description = "Maximum number of resolver rules per AWS Region"

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_rules()['ResolverRules'])

class RuleAssociationsCountCheck(QuotaCheck):
    key = "route53resolver_rule_association_count"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-94E19253'
    description = "Maximum number of associations between resolver rules and VPCs per AWS Region"

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_rule_associations()['ResolverRuleAssociations'])

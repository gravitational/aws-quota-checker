from .quota_check import QuotaCheck, QuotaScope


class MeshCountCheck(QuotaCheck):
    key = "am_mesh_count"
    scope = QuotaScope.ACCOUNT
    service_code = 'appmesh'
    quota_code = 'L-AC861A39'
    description = "Number of meshes per account"

    @property
    def current(self):
        return self.count_paginated_results("appmesh", "list_meshes", "meshes")

from .quota_check import QuotaCheck, QuotaScope


class MeshCountCheck(QuotaCheck):
    key = "am_mesh_count"
    description = "App Meshes per Account"
    scope = QuotaScope.REGION
    service_code = 'appmesh'
    quota_code = 'L-AC861A39'

    @property
    def current(self):
        return self.count_paginated_results("appmesh", "list_meshes", "meshes")

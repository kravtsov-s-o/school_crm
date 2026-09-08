from django.contrib.admin import AdminSite


class SuperuserAdminSite(AdminSite):
    """ Close DjangoAdmin only for superuser"""
    def has_permission(self, request):
        return bool(request.user.is_active and request.user.is_superuser)
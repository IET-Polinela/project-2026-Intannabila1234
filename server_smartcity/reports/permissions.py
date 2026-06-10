from rest_framework import permissions


class ReportPermission(permissions.BasePermission):
    """ACL untuk Report API antara Admin dan Citizen.

    Aturan:
    - List/Detail:
      - Admin: lihat semua report kecuali status DRAFT.
      - Citizen: lihat report non-DRAFT + own report termasuk DRAFT.
    - Create:
      - Hanya Citizen (non-staff) boleh membuat report.
    - Edit:
      - Admin hanya boleh mengubah field status.
      - Citizen hanya boleh mengubah report sendiri.
    - Delete:
      - Hanya Citizen dapat menghapus report sendiri.
      - Admin tidak boleh menghapus.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return not request.user.is_staff

        if request.method in ('PUT', 'PATCH'):
            return True

        if request.method == 'DELETE':
            return not request.user.is_staff

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return obj.status != obj.STATUS_DRAFT
            return obj.status != obj.STATUS_DRAFT or obj.reporter == request.user

        if request.method in ('PUT', 'PATCH'):
            if request.user.is_staff:
                return self._only_status_field(request)
            return obj.reporter == request.user

        if request.method == 'DELETE':
            return obj.reporter == request.user

        return False

    def _only_status_field(self, request):
        allowed_fields = {'status'}
        payload_keys = set(request.data.keys())
        return payload_keys.issubset(allowed_fields)

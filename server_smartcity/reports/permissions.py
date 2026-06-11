from rest_framework import permissions


class ReportPermission(permissions.BasePermission):
    """
    ACL Report API — Admin vs Citizen.

    ┌────────────┬──────────────────────────────────────────────────────┐
    │ Method     │ Aturan                                               │
    ├────────────┼──────────────────────────────────────────────────────┤
    │ GET (list) │ Semua user terauth. Queryset difilter di views.       │
    │ GET (obj)  │ Admin: non-DRAFT. Citizen: non-DRAFT + milik sendiri. │
    │ POST       │ Hanya Citizen (non-staff).                           │
    │ PUT/PATCH  │ Admin: hanya field status. Citizen: DRAFT milik sendiri.│
    │ DELETE     │ Citizen: DRAFT milik sendiri saja. Admin: dilarang.  │
    └────────────┴──────────────────────────────────────────────────────┘
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return not request.user.is_staff

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            # Object-level check menangani detail lebih lanjut
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # READ
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return obj.status != obj.STATUS_DRAFT
            return obj.status != obj.STATUS_DRAFT or obj.reporter == request.user

        # UPDATE
        if request.method in ('PUT', 'PATCH'):
            if request.user.is_staff:
                return self._only_status_field(request)
            # Citizen: hanya edit laporan sendiri yang masih DRAFT
            return obj.reporter == request.user and obj.status == obj.STATUS_DRAFT

        # DELETE
        if request.method == 'DELETE':
            if request.user.is_staff:
                return False   # Admin tidak boleh hapus
            return obj.reporter == request.user and obj.status == obj.STATUS_DRAFT

        return False

    @staticmethod
    def _only_status_field(request) -> bool:
        """Pastikan payload hanya berisi field 'status' (untuk admin PUT/PATCH)."""
        keys = set(request.data.keys())
        return bool(keys) and keys.issubset({'status'})

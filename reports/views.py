from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from .permissions import ReportPermission


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticated, ReportPermission)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        base_qs = Report.objects.all()

        if user.is_staff:
            return base_qs.exclude(status=Report.STATUS_DRAFT).order_by('-created_at')

        return base_qs.filter(
            ~Q(status=Report.STATUS_DRAFT) | Q(reporter=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Report
from .serializers import ReportSerializer
from .permissions import ReportPermission


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    permission_classes = (permissions.IsAuthenticated, ReportPermission)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab', None)
        base_qs = Report.objects.all()

        if tab == 'my_reports':
            return base_qs.filter(reporter=user).order_by('-updated_at')

        if tab == 'feed':
            return base_qs.filter(
                ~Q(reporter=user),
                ~Q(status=Report.STATUS_DRAFT)
            ).order_by('-updated_at')

        return base_qs.filter(
            ~Q(status=Report.STATUS_DRAFT) | Q(reporter=user)
        ).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

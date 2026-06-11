from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Report
from .serializers import ReportSerializer
from .permissions import ReportPermission


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000   # Dibuka lebar agar loadSummaryStats() bisa bypass


class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk laporan warga.

    Query params:
      ?tab=my_reports  → laporan milik user yang login (termasuk DRAFT)
      ?tab=feed        → laporan warga LAIN, non-DRAFT, diurutkan terbaru
      (kosong)         → semua non-DRAFT + DRAFT milik sendiri
    """

    serializer_class   = ReportSerializer
    pagination_class   = ReportPagination
    permission_classes = (permissions.IsAuthenticated, ReportPermission)

    def get_queryset(self):
        user = self.request.user
        tab  = self.request.query_params.get('tab')
        qs   = Report.objects.all()  # ordering sudah diset di Meta model

        if tab == 'my_reports':
            return qs.filter(reporter=user)

        if tab == 'feed':
            # Warga lain yang sudah mengajukan (bukan DRAFT)
            return qs.filter(~Q(reporter=user) & ~Q(status=Report.STATUS_DRAFT))

        # Default: semua non-DRAFT + DRAFT milik sendiri
        return qs.filter(~Q(status=Report.STATUS_DRAFT) | Q(reporter=user))

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

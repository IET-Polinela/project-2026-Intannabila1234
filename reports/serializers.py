from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'description', 'reporter', 'status', 'created_at', 'updated_at', 'is_owner'
        )
        read_only_fields = ('id', 'reporter', 'created_at', 'updated_at', 'is_owner')

    def get_reporter(self, obj):
        request = self.context.get('request')
        if request is not None and request.query_params.get('tab') == 'feed':
            return 'Warga Anonim'
        return obj.reporter.username

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request is None or not getattr(request, 'user', None):
            return False
        user = request.user
        return user.is_authenticated and obj.reporter == user

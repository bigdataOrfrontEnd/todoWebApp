from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ModelUsageLog,ModelProvider
from .serializers import (
    ModelProviderListSerializer,
    ModelProviderDetailSerializer,
    ModelProviderCreateSerializer,
    ModelProviderUpdateSerializer,
    ModelUsageLogSerializer,
    ModelProviderTestSerializer,
    ModelProviderSimpleSerializer,
)
from .services import ModelProviderService
class ModelProviderViewSet(viewsets.ModelViewSet):
    
    """
    模型使用日志视图集
    提供模型使用日志的增删改查接口
    """

    def get_queryset(self):
        """
        根据请求参数过滤查询集
        支持按模型提供商ID和项目ID过滤
        """
        return ModelProvider.objects.all().prefetch_related('usage_logs')
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if(self.action=='list'):
            return ModelProviderListSerializer
        elif self.action=='retrieve':
            return ModelProviderDetailSerializer
        elif self.action=='create':
            return ModelProviderCreateSerializer
        elif self.action in ['update','partial_update']:
            return ModelProviderUpdateSerializer
        return ModelProviderDetailSerializer

    def create(self, request, *args, **kwargs):
        """创建模型提供商"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider=ModelProviderService.create_provider(serializer.validated_data)
        response_serializer=ModelProviderDetailSerializer(provider)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

class ModelUsageLogViewSet(viewsets.ModelViewSet):
    """
    模型使用日志视图集
    提供模型使用日志的增删改查接口
    """
    queryset = ModelUsageLog.objects.all()
    serializer_class = ModelUsageLogSerializer

    def get_queryset(self):
        """
        根据请求参数过滤查询集
        支持按模型提供商ID和项目ID过滤
        """
        queryset = super().get_queryset()
        provider_id = self.request.query_params.get('provider_id')
        project_id = self.request.query_params.get('project_id')
        if provider_id:
            queryset = queryset.filter(model_provider_id=provider_id)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
from .models import ModelProvider
from typing import Dict, Any, Optional, List
from django.db import transaction
class ModelProviderService:
    """
    模型提供商服务
    职责: 处理模型提供商的业务逻辑
    """
    @staticmethod
    @transaction.atomic
    def create_provider(data: Dict[str, Any]) -> ModelProvider:
        """
        创建模型提供商

        Args:
            data: 提供商数据

        Returns:
            创建的模型提供商实例
        """
        provider = ModelProvider.objects.create(**data)
        return provider

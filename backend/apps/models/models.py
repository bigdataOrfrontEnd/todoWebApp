import uuid
from django.db import models
class ModelProvider(models.Model):
    """
    模型提供商
    职责: 存储AI模型的配置信息
    """
    PROVIDER_TYPES=[
          ('llm', 'LLM模型'),
          ('text2image', '文生图模型'),
          ('image2video', '图生视频模型'),
          ]
     # 执行器选项定义
    LLM_EXECUTORS = [
        ('core.ai_client.openai_client.OpenAIClient', 'OpenAI兼容客户端'),
    ]

    TEXT2IMAGE_EXECUTORS = [
        ('core.ai_client.text2image_client.Text2ImageClient', '文生图客户端'),
        ('core.ai_client.comfyui_client.ComfyUIClient', 'ComfyUI客户端'),
    ]

    IMAGE2VIDEO_EXECUTORS = [
        ('core.ai_client.image2video_client.Image2VideoClient', '图生视频客户端'),
        ('core.ai_client.comfyui_client.ComfyUIClient', 'ComfyUI客户端'),
    ]
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255, verbose_name="模型提供商名称")
    provider_type=models.CharField(max_length=50, verbose_name="提供商类型",choices=PROVIDER_TYPES)  
    executor_class=models.CharField(max_length=255,
                                      help_text='执行器的完整类路径，如: core.ai_client.openai_client.OpenAIClient',
                                      verbose_name="执行器类",
                                      blank=True,
                                      default=''
                                      )# 例如: OpenAI, HuggingFace
    api_url = models.URLField(verbose_name="API地址")
    api_key = models.CharField(max_length=512, verbose_name="API密钥")
    model_name = models.CharField(max_length=255, verbose_name="模型名称")
    # LLM专用参数
    max_tokens = models.IntegerField(null=True, blank=True, verbose_name="最大令牌数",default=2000)
    temperature = models.FloatField(null=True, blank=True, verbose_name="温度",default=0.7)
    top_p = models.FloatField(null=True, blank=True, verbose_name="Top P值",default=1.0)
    # 通用参数
    timeout=models.IntegerField(null=True, blank=True, verbose_name="请求超时(秒)",default=60)
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    priority = models.IntegerField(default=0, verbose_name="优先级",help_text='用于负载均衡')
    # 限流配置
    rate_limit_rpm=models.IntegerField(null=True, blank=True, verbose_name="每分钟请求数限制",default=60)
    rate_limit_rpd=models.IntegerField(null=True, blank=True, verbose_name="每天请求数限制",default=1000)
    # 额外配置 (JSON格式,存储特定模型的额外参数)
    extra_config=models.JSONField(null=True, blank=True, verbose_name="额外配置")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新时间")
    #显示表的信息
    class Meta:
        db_table = 'model_providers'
        verbose_name = '模型提供商'
        verbose_name_plural = '模型提供商'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['provider_type', 'is_active', '-priority']),
        ]
    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"
    
    def get_executor_choices(self):
        """
        获取可用的执行器类选择
        """
        executor_map = {
            'llm': self.LLM_EXECUTORS,
            'text2image': self.TEXT2IMAGE_EXECUTORS,
            'image2video': self.IMAGE2VIDEO_EXECUTORS,
        }
        return executor_map.get(self.provider_type, [])
    
    def get_default_executor(self):
        """
        获取默认的执行器类
        """
        executor_choices = self.get_executor_choices()
        if executor_choices:
            return executor_choices[0][0]
        return ''
    def validate_executor_class(self):
        """
        验证所选的执行器类是否有效
        """
        if not self.executor_class:
            return False
        vialid_executors = [choice[0] for choice in self.get_executor_choices()]
        return self.executor_class in vialid_executors

class ModelUsageLog(models.Model):
    """
    模型使用日志
    职责: 记录模型调用历史,用于统计和成本计算
    """
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    model_provider=models.ForeignKey(ModelProvider, on_delete=models.CASCADE,related_name='usage_logs', verbose_name="模型提供商")
    
    # 使用信息
    request_data=models.JSONField(verbose_name="请求数据",default=dict)
    response_data=models.JSONField(verbose_name="响应数据",default=dict)

    # 统计信息
    tokens_used=models.IntegerField(null=True, blank=True, verbose_name="使用Token数",default=0)
    latency_ms=models.IntegerField(null=True, blank=True, verbose_name="延迟(毫秒)",default=0)
    status=models.CharField(max_length=50, verbose_name="状态",default='success')  # success, failed
    error_message=models.TextField(null=True, blank=True, verbose_name="错误信息")

    # 关联信息
    project_id=models.UUIDField(null=True, blank=True, verbose_name="项目ID")
    stage_type=models.CharField(max_length=50, null=True, blank=True, verbose_name="阶段类型")  # e.g., 'development', 'production'
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'model_usage_logs'
        verbose_name = '模型使用日志'
        verbose_name_plural = '模型使用日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['model_provider', '-created_at']),
            models.Index(fields=['project_id', 'stage_type']),
        ]
    def __str__(self):
        return f'{self.model_provider.name} - {self.created_at}'
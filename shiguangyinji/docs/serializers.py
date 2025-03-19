from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'public', 'owner_id']

    def create(self, validated_data):
        user = self.context['request'].user  # 获取当前请求的用户
        validated_data['owner_id'] = user  # 自动设置文档的 owner 字段
        return super().create(validated_data)

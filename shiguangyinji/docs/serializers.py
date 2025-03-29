from rest_framework import serializers
from tutorial.quickstart.serializers import UserSerializer

from .models import Document, Like, Comment


class DocumentSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'public', 'owner_id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner_id'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print("传入的更新数据:", validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user_id', 'created_at', 'content']
        # 如果需要支持空值，确保字段允许空值
        extra_kwargs = {
            'user_id': {'required': False, 'allow_null': True},
            'created_at': {'required': False, 'allow_null': True},
            'content': {'required': True}
        }



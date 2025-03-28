from rest_framework import serializers
from .models import Document, Like


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
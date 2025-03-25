# views.py
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from django.utils.dateparse import parse_date
import logging

logger = logging.getLogger(__name__)


class CreateDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        serializer = DocumentSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  # 创建文档并保存
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"msg": "创建文档失败", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListUserDocumentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        documents = Document.objects.filter(owner_id=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


class DeleteDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, doc_id):
        try:
            document = Document.objects.get(id=doc_id, owner_id=request.user)
            document.delete()
            return Response({"success": True, "msg": "文档删除成功"}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({"msg": "文档不存在或无权限删除"}, status=status.HTTP_404_NOT_FOUND)


class EditDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, doc_id):
        try:
            document = Document.objects.get(id=doc_id, owner_id=request.user)
        except Document.DoesNotExist:
            return Response({"msg": "文档不存在或无权限编辑"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentSerializer(document, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"msg": "更新失败", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DocumentCreatedAtView(APIView):
    def get(self, request, *args, **kwargs):
        documents = Document.objects.all()
        return Response({"created_at": [doc.created_at for doc in documents]}, status=status.HTTP_200_OK)


class ListDocsByDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        date_str = kwargs.get('date')  # 从路径中获取日期

        if not date_str:
            return Response({"success": False, "error": "Missing date parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = parse_date(date_str)
            print(date)
            if not date:
                return Response({"success": False, "error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

            # 从数据库中查询匹配的文档
            docs = Document.objects.filter(created_at=date, owner_id=request.user)

            # 如果没有找到文档，返回空数据
            if not docs.exists():
                print("null")
                return Response({"success": True, "data": []}, status=status.HTTP_200_OK)

            # 序列化文档数据
            serializer = DocumentSerializer(docs, many=True)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred while retrieving documents: {e}")
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

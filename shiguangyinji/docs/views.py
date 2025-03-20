# views.py
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer


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
from django.urls import path
from .views import CreateDocumentView, ListUserDocumentsView, DeleteDocumentView

urlpatterns = [
    path('create/', CreateDocumentView.as_view(), name='create-document'),
    path('myDocs/', ListUserDocumentsView.as_view(), name='user-documents'),
    path('delete/<int:doc_id>/', DeleteDocumentView.as_view(), name='delete-document'),
]
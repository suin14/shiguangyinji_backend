from django.urls import path
from .views import CreateDocumentView, ListUserDocumentsView, DeleteDocumentView, EditDocumentView, \
    DocumentCreatedAtView, ListDocsByDateView, RetrieveDocumentView

urlpatterns = [
    path('create/', CreateDocumentView.as_view(), name='create-document'),
    path('myDocs/', ListUserDocumentsView.as_view(), name='user-documents'),
    path('delete/<int:doc_id>/', DeleteDocumentView.as_view(), name='delete-document'),
    path('edit/<int:doc_id>/', EditDocumentView.as_view(), name='edit-document'),
    path('get_created_at/', DocumentCreatedAtView.as_view(), name='document-created-at'),
    path('list_docs_by_date/<str:date>/', ListDocsByDateView.as_view(), name='list_docs_by_date'),
    path('get_document/<int:doc_id>/', RetrieveDocumentView.as_view(), name='get_document_by_id'),
]

from django.urls import path
from .views import CreateDocumentView, ListUserDocumentsView, DeleteDocumentView, EditDocumentView, \
    DocumentCreatedAtView, ListDocsByDateView, RetrieveDocumentView, \
    CheckUserLikeView, LikeDocView, GetDocLikeCountView, FavoriteArticleView, CheckUserFavoriteView, \
    UserFavoriteListView, CommentView

urlpatterns = [
    path('create/', CreateDocumentView.as_view(), name='create-document'),
    path('myDocs/', ListUserDocumentsView.as_view(), name='user-documents'),
    path('delete/<int:doc_id>/', DeleteDocumentView.as_view(), name='delete-document'),
    path('edit/<int:doc_id>/', EditDocumentView.as_view(), name='edit-document'),
    path('get_created_at/', DocumentCreatedAtView.as_view(), name='document-created-at'),
    path('list_docs_by_date/<str:date>/', ListDocsByDateView.as_view(), name='list_docs_by_date'),
    path('get_document/<int:doc_id>/', RetrieveDocumentView.as_view(), name='get_document_by_id'),
    path('<int:doc_id>/like/', LikeDocView.as_view(), name='like_doc'),
    path('<int:docid>/like/count/', GetDocLikeCountView.as_view(), name='get_doc_like_count'),
    path('<int:doc_id>/like/check/', CheckUserLikeView.as_view(), name='check_like'),
    path('<int:doc_id>/favorite/', FavoriteArticleView.as_view(), name='favorite-article'),
    path('<int:doc_id>/favorite/check/', CheckUserFavoriteView.as_view(), name='check-favorite'),
    path('favorites/', UserFavoriteListView.as_view(), name='user-favorites'),
    path('<int:doc_id>/comments/', CommentView.as_view(), name='article-comments'),
]

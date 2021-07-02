from django.urls    import path

from likes.views import LikeView
from postings.views import (
    WritePostView, 
    PostsView, 
    WriteCommentView, 
    CommentsView, 
    AllPostsView
)

urlpatterns = [
    path('/write', WritePostView.as_view()),
    path('/<int:post_pk>/comments/write', WriteCommentView.as_view()),
    path('/<int:pk>', PostsView.as_view()),
    path('/all', AllPostsView.as_view()),
    path('/<int:post_pk>/comments/<int:comment_pk>', CommentsView.as_view()),
    path('/<int:post_pk>/like', LikeView.as_view())
]
from django.urls    import path

from postings.views import (
    WritePostView, 
    PostsView, 
    WriteCommentView, 
    CommentsView, 
    AllPostsView
)

urlpatterns = [
    path('/write', WritePostView.as_view()),
    path('/<int:postpk>/writecomment', WriteCommentView.as_view()),
    path('/<int:pk>', PostsView.as_view()),
    path('/all', AllPostsView.as_view()),
    path('/<int:postpk>/comments', CommentsView.as_view()),
]
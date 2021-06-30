from django.urls    import path

from postings.views import WritePostView, PostsView, WriteCommentView

urlpatterns = [
    path('/write', WritePostView.as_view()),
    path('/posts', PostsView.as_view()),
    path('/writecomment', WriteCommentView.as_view()),
]
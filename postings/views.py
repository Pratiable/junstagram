import json

from django.db.utils import IntegrityError
from django.utils    import timezone
from django.http     import JsonResponse
from django.views    import View

from postings.models import Post, Image, Comment, Like
from authorization   import Authorize
from user.models     import User

class WritePostView(View):
    @Authorize
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not data['images']:
                return JsonResponse({'MESSAGE':'IMAGE_REQUIRED'}, status=400)

            signed_user = request.user

            post = Post.objects.create(
                author  = signed_user,
                content = data['content']
            )
            image_list = [
                Image(post=post, url=image)
                for image in data['images']
            ]
            Image.objects.bulk_create(image_list)

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVAILED_USER'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)

class AllPostsView(View):
    def get(self, request):
        posts   = Post.objects.all()
        results = []
        for post in posts: 
            images     = post.image_set.all()
            image_list = [image.url for image in images]
            results.append(
                {
                    'author'    : post.author.nickname,
                    'content'   : post.content,
                    'created_at': 
                    timezone.localtime(post.created_at).strftime("%Y-%m-%dT%H:%M:%S"),
                    'images'    : image_list,
                    'likes'     : len(Like.objects.filter(post=post))
                }
            )
        return JsonResponse({'Posts': results}, status=200)

class PostsView(View):
    @Authorize
    def get(self, request, pk):
        post        = Post.objects.get(pk=pk)
        signed_user = request.user
        images      = post.image_set.all()
        image_list  = [image.url for image in images]
        
        comments      = post.comment_set.all()
        comments_list = []
        
        post_view = {
            'author'    : post.author.nickname,
            'content'   : post.content,
            'created_at': 
            timezone.localtime(post.created_at).strftime("%Y-%m-%dT%H:%M:%S"),
            'images'    : image_list,
            'likes'     : len(Like.objects.filter(post_id=pk)),
            'user_like' : bool(Like.objects.filter(post_id=pk, user=signed_user)),
        }
        for comment in comments:
            comments_list.append(
                {
                'user'      : comment.user.nickname,
                'content'   : comment.content,
                'created_at': 
                timezone.localtime(post.created_at).strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )

        return JsonResponse({'Post': post_view, 'Comments': comments_list}, status=200)

    @Authorize
    def delete(self, request, pk):
        try:
            signed_user = request.user
            post = Post.objects.get(pk=pk)

            if post.author == signed_user:
                post.delete()
                return JsonResponse({"MESSAGE":"POST_DELETED"}, status=200)
            return JsonResponse({"MESSAGE":"PERMISSION_DENIED"}, status=400)
            
        except Post.DoesNotExist:
            return JsonResponse({"MESSAGE":"POST_NOT_EXISTS"}, status=400)
    
    @Authorize
    def patch(self, request, pk):
        try:
            data = json.loads(request.body)
            signed_user = request.user
            post = Post.objects.get(pk=pk)

            if post.author == signed_user:
                post.update(content = data['content'])
                return JsonResponse({"MESSAGE":"UPDATE_SUCCESS"}, status=200)
            return JsonResponse({"MESSAGE":"PERMISSION_DENIED"}, status=400)

        except Post.DoesNotExist:
            return JsonResponse({"MESSAGE":"POST_NOT_EXISTS"}, status=400)
        except:
            return JsonResponse({"MESSAGE":"ERROR"}, status=400)
            


class WriteCommentView(View):
    @Authorize
    def post(self, request, post_pk):
        try:
            data        = json.loads(request.body)
            signed_user = request.user
            post        = Post.objects.get(pk=post_pk)
            
            if not data['content']:
                return JsonResponse({"MESSAGE":"NEED_CONTENTS"}, status=400)

            comment = Comment.objects.create(
                user    = signed_user,
                post    = post,
                content = data['content']
            )
            if 'nested_comment' in data:
                parent_comment = Comment.objects.get(id=data['nested_comment'])

                if parent_comment.nested_comment:
                    comment.nested_comment = parent_comment.nested_comment
                    comment.save()
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

                comment.nested_comment_id = data['nested_comment']
                comment.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        
        except IntegrityError:
            return JsonResponse({'MESSAGE':'FOREIGN_KEY_ERROR'}, status=400)

class CommentsView(View):
    def get(self, request, post_pk):
        comments = Comment.objects.filter(post_id=post_pk)
        results  = []
        for comment in comments:
            results.append(
                {
                'content'   : comment.content,
                'user'      : comment.user.nickname,
                'created_at': 
                timezone.localtime(comment.created_at).strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        return JsonResponse({"COMMENTS" : results}, status=200)
    
    @Authorize
    def delete(self, request, comment_pk):
        signed_user = request.user
        try:
            comment = Comment.objects.get(pk=comment_pk)

            if comment.user == signed_user:
                comment.delete()
                return JsonResponse({"MESSAGE":"COMMENT_DELETED"}, status=200)
            return JsonResponse({"MESSAGE":"PERMISSION_DENIED"}, status=400)

        except Comment.DoesNotExist:
            return JsonResponse({"MESSAGE":"COMMENT_NOT_EXISTS"}, status=400)

class LikeView(View):
    @Authorize
    def get(self, request, postpk):
        signed_user = request.user

        if Like.objects.filter(user=signed_user, post_id=postpk).exists():
            Like.objects.get(user=signed_user, post_id=postpk).delete()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)

        Like.objects.create(
            user    = signed_user,
            post_id = postpk
        )
        return JsonResponse({"MESSAGE":"SUCCESS"}, status = 201)
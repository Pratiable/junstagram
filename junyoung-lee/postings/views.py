import json

from django.db.utils import IntegrityError
from django.utils    import timezone
from django.http     import JsonResponse
from django.views    import View

from postings.models import Post, Image, Comment
from postings.decoder import TokenChecker
from user.models     import User

class WritePostView(View):
    @TokenChecker
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not data['images']:
                return JsonResponse({'MESSAGE':'IMAGE_REQUIRED'}, status=400)

            post = Post.objects.create(
                author  = User.objects.get(pk=data['user_id']),
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

class PostsView(View):
    @TokenChecker
    def get(self, request):
        posts = Post.objects.all()
        results = []
        for post in posts:
            images = post.image_set.all()
            image_list = [image.url for image in images]
            results.append(
                {
                    'author'    : post.author.nickname,
                    'content'   : post.content,
                    'created_at': 
                    timezone.localtime(post.created_at).strftime("%Y-%m-%dT%H:%M:%S"),
                    'images'    : image_list,
                }
            )
        return JsonResponse({'Posts': results}, status=200)

class WriteCommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment = Comment.objects.create(
                user_id = data['user'],
                post_id = data['post'],
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

# class CommentsView(View):
#     def get(self, request):
#         Post.objects.get()

# 쿼리셋에서 닉네임 가져오기
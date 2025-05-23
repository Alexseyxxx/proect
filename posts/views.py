import logging

from typing import Literal
from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseBadRequest
from django.shortcuts import render, redirect
from posts.models import Posts, Images, Categories, PostReaction
from django.conf import settings

logger = logging.getLogger()


class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active
            }
        )


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        categories = Categories.objects.all()
        if not categories:
            return HttpResponse(
                content="<h1>Something went wrong</h1>"
            )
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, template_name="post_form.html",
            context={"categories": categories}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        images = request.FILES.getlist("images")
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) for img in images]
        Images.objects.bulk_create(imgs)
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        return redirect(to="base")


class ShowDeletePostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            post = None
        author = False
        if request.user == post.user:
            author = True
        return render(
            request=request, template_name="pk_post.html",
            context={
                "post": post,
                "author": author
            }
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            pass
        if request.user != post.user:
            return HttpResponse(
                "<h1>У тебя здесь нет власти</h1>"
            )
        post.delete()
        return redirect(to="base")

class LikesView(View):
    def post(self, request: HttpRequest, pk: int, action: Literal["like", "dislike"]):
        client = request.user
        if not client.is_authenticated:
            return JsonResponse({"error": "Пользователь не авторизован"}, status=403)

        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Пост не найден"}, status=404)

        reaction = PostReaction.objects.filter(user=client, post=post).first()
        opposite = "dislike" if action == "like" else "like"

        # Удаление реакции при повторном нажатии
        if reaction and reaction.reaction == action:
            setattr(post, f"{action}s", max(0, getattr(post, f"{action}s") - 1))
            reaction.delete()
        else:
            # Изменение реакции
            if reaction:
                setattr(post, f"{reaction.reaction}s", max(0, getattr(post, f"{reaction.reaction}s") - 1))
                setattr(post, f"{action}s", getattr(post, f"{action}s") + 1)
                reaction.reaction = action
                reaction.save()
            else:
                PostReaction.objects.create(user=client, post=post, reaction=action)
                setattr(post, f"{action}s", getattr(post, f"{action}s") + 1)

        post.save(update_fields=["likes", "dislikes"])
        return redirect('pk_post', pk=pk)
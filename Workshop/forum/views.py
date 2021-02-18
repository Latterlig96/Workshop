from http import HTTPStatus
from typing import Dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from shop.models import Employee, Owner
from .forms import CommentsForm, CreateForumForm, CreatePostForm, CreateThreadForm
from .models import Comments, Forum, Post, Thread
from .utils import is_employee, is_owner


@login_required
@permission_required('shop.can_create_forum')
def create_forum(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        forum_form = CreateForumForm(request.POST)
        if forum_form.is_valid():
            cd: Dict = forum_form.cleaned_data
            new_forum = Forum.objects.create(title=cd['title'],
                                             description=cd['description'],
                                             threads=0,
                                             posts=0)
            new_forum.add(cd['group'])
            messages.success(request, "Forum has been successfully created")
            return redirect('owner_dashboard')
    else:
        forum_form = CreateForumForm()
        return render(request,
                      'forum/create_forum.html',
                      {'form': forum_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_create_thread')
def create_thread(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        thread_form = CreateThreadForm(request.POST)
        if thread_form.is_valid():
            cd: Dict = thread_form.cleaned_data
            new_thread = Thread.objects.create(forum=cd['forum'],
                                               title=cd['title'],
                                               posts=0,
                                               views=0,
                                               closed=False)
            forum = Forum.objects.get(id=new_thread.forum.id)
            forum.threads += 1
            forum.save()
            messages.success(request, "Thread has been successfully added")
            return redirect('forum_dashboard')
    else:
        thread_form = CreateThreadForm()
        return render(request,
                      'forum/create_thread.html',
                      {'form': thread_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_create_post')
def create_post(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        post_form = CreatePostForm(request.POST)
        if post_form.is_valid():
            cd: Dict = post_form.cleaned_data
            new_post = Post.objects.create(thread=cd['thread'],
                                           author=cd['author'],
                                           body=cd['body'])
            thread = Thread.objects.get(id=new_post.thread.id)
            thread.posts += 1
            thread.save()
            forum = Forum.objects.get(id=thread.forum.id)
            forum.posts += 1
            forum.save()
            messages.success(request, "Post has been successfully added")
            return redirect('forum_dashboard')
    else:
        post_form = CreatePostForm()
        return render(request,
                      'forum/create_post.html',
                      {'form': post_form},
                      status=HTTPStatus.OK)


@login_required
def forum_dashboard(request: WSGIRequest) -> HttpResponse:
    if is_employee(request.user):
        employee = Employee.objects.get(employee=request.user)
        forums = Forum.objects.filter(shop=employee.shop).all()
    if is_owner(request.user):
        owner = Owner.objects.get(owner=request.user)
        forums = Forum.objects.filter(shop=owner.shop).all()
    return render(request,
                  'forum/forum_dashboard.html',
                  {'forums': forums},
                  status=HTTPStatus.OK)


@login_required
def thread_list(request: WSGIRequest,
                id: int
                ) -> HttpResponse:
    threads = Thread.objects.filter(forum__id=id).all()
    return render(request,
                  'forum/thread_list.html',
                  {'threads': threads},
                  status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_view_thread')
def thread_detail(request: WSGIRequest,
                  id: int
                  ) -> HttpResponse:
    thread = Thread.objects.get(id=id)
    posts = Post.objects.filter(thread__id=thread.id).all()
    return render(request,
                  'forum/thread_detail.html',
                  {'thread': thread,
                   'posts': posts},
                  status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_view_post')
def post_detail(request: WSGIRequest,
                id: int
                ) -> HttpResponse:
    post = Post.objects.get(id=id)
    comments = Comments.objects.filter(post=post).all()
    if request.method == "POST":
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            cd: Dict = comments_form.cleaned_data
            Comments.objects.create(from_user=request.user,
                                    post=post,
                                    body=cd['body'])
            messages.success(request, "Comment sucessfully added")
            return redirect('post_detail', id=post.id)
    else:
        comments_form = CommentsForm()
    return render(request,
                  'forum/post_detail.html',
                  {'post': post,
                   'form': comments_form,
                   'comments': comments},
                  status=HTTPStatus.OK)

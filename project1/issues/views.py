from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Issue, Comment
from .forms import IssueForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# Create your views here.
@login_required
def index(request):
    sort = request.GET.get('sort', '')
    if sort == 'views':
        issues = Issue.objects.all().order_by('-count')
    elif sort == 'recently':
        issues = Issue.objects.all().order_by('-created_at')
    elif sort == 'unRecently':
        issues = Issue.objects.all().order_by('created_at')
    else:
        issues = Issue.objects.all()
    
    paginator = Paginator(issues,10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'issues': posts,
    }
    return render(request, 'issues/index.html', context)

@login_required
def detail(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.count += 1
    issue.save()
    comment_form = CommentForm()
    comments = issue.comments_issue.all()
    context = {
        'issue': issue,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'issues/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            form.save()
            return redirect('issues:detail', issue.pk)
    else:
        form = IssueForm()
    context = {
        'form': form,
    }
    return render(request, 'issues/create.html', context)


@login_required
def delete(request, pk):
    issue = Issue.objects.get(pk=pk)
    if request.user == issue.user:
        issue.delete()
    return redirect('issues:index')


@login_required
def update(request, pk):
    issue = Issue.objects.get(pk=pk)
    if request.user == issue.user:
        if request.method == 'POST':
            form = IssueForm(request.POST, request.FILES, instance=issue)
            if form.is_valid:
                p = form.save(commit=False)
                p.user = request.user
                form.save()
                return redirect('issues:detail', issue.pk)
        else:
            form = IssueForm(request.FILES, instance=issue)
    else:
        return redirect('issues:index')
    context = {
        'issue': issue,
        'form': form,
    }
    return render(request, 'issues/update.html', context)


@login_required
def comments_create(request, pk):
    issue = Issue.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.issue = issue
        comment.comment_user = request.user
        comment_form.save()
        return redirect('issues:detail', issue.pk)
    context = {
        'issue': issue,
        'comment_form': comment_form,
        'comment' : comment
    }
    return render(request, 'issues/detail.html', context)


def comments_delete(request, issue_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.comment_user:
        comment.delete()
    # return redirect('issues:detail', issue_pk)
    context = {

    }
    return JsonResponse(context)


def likes(request, issue_pk):
    issue = Issue.objects.get(pk=issue_pk)
    # if issue.like_users.filter(pk=request.user.pk).exists():
    #     issue.like_users.remove(request.user)
    # else:
    if not issue.like_users.filter(pk=request.user.pk):
        issue.like_users.add(request.user)
        is_liked = True
    else:
        issue.like_users.remove(request.user)
        is_liked = False

    issue.save()

    context = {
        'is_liked': is_liked,
        'likes_count': issue.like_users.count()
    }
    
    # return redirect('issues:detail', issue_pk)
    return JsonResponse(context)


def likes_comment(request, issue_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # if issue.like_users.filter(pk=request.user.pk).exists():
    #     issue.like_users.remove(request.user)
    # else:
    if request.user not in comment.like_comment_users.all():
        comment.like_comment_users.add(request.user)
        is_comment_liked = True
    else:
        comment.like_comment_users.remove(request.user)
        is_comment_liked = False

    comment.save()

    context = {
        'is_comment_liked': is_comment_liked,
        'comment_likes_count': comment.like_comment_users.count()
    }
    
    # return redirect('issues:detail', issue_pk)
    return JsonResponse(context)


def issue_list(request):
    all_issues  = Issue.objects.all()
   
    page = request.GET.get('page', 1)
    paginator = Paginator(all_issues, 10)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)

    context = {
        'samelines' : lines,
    }
 
    return render(request, 'issues/index.html', context)
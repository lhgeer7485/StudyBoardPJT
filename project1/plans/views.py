from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan, Comment
from .forms import PlanForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# Create your views here.
@login_required
def index(request):
    sort = request.GET.get('sort', '')
    if sort == 'views':
        plans = Plan.objects.all().order_by('-count')
    elif sort == 'recently':
        plans = Plan.objects.all().order_by('-created_at')
    elif sort == 'unRecently':
        plans = Plan.objects.all().order_by('created_at')
    else:
        plans = Plan.objects.all()
    paginator = Paginator(plans,10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'plans': posts,
    }
    return render(request, 'plans/index.html', context)

@login_required
def detail(request, pk):
    plan = Plan.objects.get(pk=pk)
    plan.count += 1
    plan.save()
    comment_form = CommentForm()
    comments = plan.comments.all()
    context = {
        'plan': plan,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'plans/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            form.save()
            return redirect('plans:detail', plan.pk)
    else:
        form = PlanForm()
    context = {
        'form': form,
    }
    return render(request, 'plans/create.html', context)


@login_required
def delete(request, pk):
    plan = Plan.objects.get(pk=pk)
    if request.user == plan.user:
        plan.delete()
    return redirect('plans:index')


@login_required
def update(request, pk):
    plan = Plan.objects.get(pk=pk)
    if request.user == plan.user:
        if request.method == 'POST':
            form = PlanForm(request.POST, request.FILES, instance=plan)
            if form.is_valid:
                p = form.save(commit=False)
                p.user = request.user
                form.save()
                return redirect('plans:detail', plan.pk)
        else:
            form = PlanForm(request.FILES, instance=plan)
    else:
        return redirect('plans:index')
    context = {
        'plan': plan,
        'form': form,
    }
    return render(request, 'plans/update.html', context)


@login_required
def comments_create(request, pk):
    plan = Plan.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.plan = plan
        comment.comment_user = request.user
        comment_form.save()
        return redirect('plans:detail', plan.pk)
    context = {
        'plan': plan,
        'comment_form': comment_form,
        'comment' : comment
    }
    return render(request, 'plans/detail.html', context)


def comments_delete(request, plan_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.comment_user:
        comment.delete()
    # return redirect('plans:detail', plan_pk)
    context = {

    }
    return JsonResponse(context)


def likes(request, plan_pk):
    plan = Plan.objects.get(pk=plan_pk)
    # if plan.like_users.filter(pk=request.user.pk).exists():
    #     plan.like_users.remove(request.user)
    # else:
    if not plan.like_users.filter(pk=request.user.pk):
        plan.like_users.add(request.user)
        is_liked = True
    else:
        plan.like_users.remove(request.user)
        is_liked = False

    plan.save()

    context = {
        'is_liked': is_liked,
        'likes_count': plan.like_users.count()
    }
    
    # return redirect('plans:detail', plan_pk)
    return JsonResponse(context)


def likes_comment(request, plan_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # if plan.like_users.filter(pk=request.user.pk).exists():
    #     plan.like_users.remove(request.user)
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
    
    # return redirect('plans:detail', plan_pk)
    return JsonResponse(context)


def plan_list(request):
    all_plans  = Plan.objects.all()
   
    page = request.GET.get('page', 1)
    paginator = Paginator(all_plans, 10)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)

    context = {
        'samelines' : lines,
    }
 
    return render(request, 'plans/index.html', context)
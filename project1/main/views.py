from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Main
from plans.models import Plan
from issues.models import Issue
from challenges.models import Challenge
from algorithms.models import Algorithm
from datetime import datetime
from .forms import MainForm, CommentForm
# Create your views here.
def index(request):
    mains = Main.objects.all()
    plans = Plan.objects.all()
    challenges = Challenge.objects.all()
    issues = Issue.objects.all()
    algorithms = Algorithm.objects.all()
    now = datetime.now()
    today_challenge = []
    for challenge in challenges:
        if challenge.created_at.date() == now.date():
            today_challenge.append(challenge)
    context = {
        'mains': mains,
        'plans': plans,
        'challenges' : today_challenge,
        'issues' : issues,
        'algorithms' : algorithms,
    }
    return render(request, 'main/index.html', context)


def detail(request, pk):
    main = Main.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = main.comment_set.all()
    context = {
        'main': main,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'main/detail.html', context)

def test(request):
    mains = Main.objects.all()
    context = {
        'mains': mains,
    }
    return render(request, 'main/test.html', context)

def test2(request):
    mains = Main.objects.all()
    context = {
        'mains': mains,
    }
    return render(request, 'main/test2.html', context)
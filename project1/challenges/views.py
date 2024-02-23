from django.shortcuts import render,redirect
from .models import Challenge,Code
from algorithms.models import Problem
from django.core.paginator import Paginator #페이지네이션 구현 모듈
from .forms import ChallengeForm, CodeForm
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            problem = Problem.objects.get(problem_num=challenge.problem)
            challenge.rank = problem.rank
            challenge.title = problem.name
            form.save()
            return redirect('challenges:index')
    else:
        form = ChallengeForm()
    now = timezone.now()
    challenges = Challenge.objects.all().order_by('-created_at')
    for challenge in challenges:
        if challenge.created_at.date() == now.date():
            challenge.is_today = 1
        else:
            challenge.is_today = 0
    # 페이지네이션 객체(paginator)
    paginator = Paginator(challenges,3) # challenge 리스트 3개 단위로 잘라 보여줌
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'challenges' : posts,
     
        'form' : form,
    }
    
    return render(request,'challenges/index.html',context)

def detail(request,challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    codes = challenge.code_challenges.all().order_by('-created_at')
    paginator = Paginator(codes,3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    print(codes)
    problem = Problem.objects.get(problem_num=challenge.problem)
    context = {
        'challenge' : challenge,
        'problem' : problem,
        'codes' : posts
        
    }
    return render(request,'challenges/detail.html',context)

@login_required
def code(request,challenge_pk):
    if request.method =='POST':
        code_text = Code()
        code_text.content = request.POST['editor']
        code_text.challenge = Challenge.objects.get(pk=challenge_pk)
        challenge = Challenge.objects.get(pk=challenge_pk)
        
        code_text.author = request.user
        code_text.save()
        return redirect('challenges:index')
    else:
        print('bye')
        challenge = Challenge.objects.get(pk=challenge_pk)
        
        context=  {
            'challenge' : challenge
        }
        return render(request,'challenges/code.html',context)
    
def watch(request,code_pk):
    code = Code.objects.get(pk=code_pk)
    context = {
        'code' : code,
    }
    return render(request,'challenges/watch.html', context)
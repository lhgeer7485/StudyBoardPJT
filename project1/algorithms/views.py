from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Problem, ProblemClass, Algorithm
from .crawling import solved_crawling as sc
from .forms import AlgorithmFrom
import datetime

rank_list = ['', 'B5', 'B4', 'B3', 'B2', 'B1', 'S5', 'S4', 'S3', 'S2', 'S1',  
            'G5', 'G4', 'G3', 'G2', 'G1', 'P5', 'P4', 'P3', 'P2', 'P1',
            'D5', 'D4', 'D3', 'D2', 'D1', 'R5', 'R4', 'R3', 'R2', 'R1']


rank_dic = {
    'Sprout' : 'B5','Unrated' : 'UR',
    'Bronze V' : 'B5', 'Bronze IV' : 'B4', 'Bronze III' : 'B3', 'Bronze II' : 'B2', 'Bronze I' : 'B1',
    'Silver V' : 'S5', 'Silver IV' : 'S4', 'Silver III' : 'S3', 'Silver II' : 'S2', 'Silver I' : 'S1',
    'Gold V' : 'G5', 'Gold IV' : 'G4', 'Gold III' : 'G3', 'Gold II' : 'G2', 'Gold I' : 'G1',
    'Platinum V' : 'P5', 'Platinum IV' : 'P4', 'Platinum III' : 'P3', 'Platinum II' : 'P2', 'Platinum I' : 'P1',
    'Diamond V' : 'D5', 'Diamond IV' : 'D4', 'Diamond III' : 'D3', 'Diamond II' : 'D2', 'Diamond I' : 'D1',
    'Ruby V' : 'R5', 'Ruby IV' : 'R4', 'Ruby III' : 'R3', 'Ruby II' : 'R2','Ruby I' : 'R1',
}


# 유저가 푼 문제를 보여주는 사이트를 랜더하는 함수
def solved(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    solved_problems = person.solved_problems.all()
    rank_dic = {'B' : 0, 'S' : 0, 'G' : 0, 'P' : 0, 'D' : 0, 'R' : 0,'UR' : 0,}
    class_dic = {

    }

    # django aggregate and django join 공부하기
    for solved_problem in solved_problems:
        if solved_problem.rank[0] == 'B':
            rank_dic['B'] += 1
        elif solved_problem.rank[0] == 'S':
            rank_dic['S'] += 1
        elif solved_problem.rank[0] == 'G':
            rank_dic['G'] += 1
        elif solved_problem.rank[0] == 'P':
            rank_dic['P'] += 1
        elif solved_problem.rank[0] == 'D':
            rank_dic['D'] += 1
        elif solved_problem.rank[0] == 'R':
            rank_dic['R'] += 1
        elif solved_problem.rank[0] == 'U':
            rank_dic['UR'] += 1

        for classs in solved_problem.classes.all():
            class_dic[classs.name] = class_dic.setdefault(classs.name, 0) + 1

    graph_list = [class_dic['자료 구조'],class_dic['다이나믹 프로그래밍'],class_dic['그리디 알고리즘'],class_dic['브루트포스 알고리즘'],class_dic['그래프 이론'],class_dic['문자열']]
#
    print(graph_list)
# 
    context = {
        'person' : person,
        'rank_dic' : rank_dic,
        'class_dic' : class_dic,
        'graph_list' : graph_list,
    }


    return render(request,'algorithms/test.html', context)


# 닉네임에 해당하는 유저 프로필에서 푼 문제들과 랭크를 가져오는 크롤링
def solved_crawling(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    sc(person)
    return redirect('algorithms:solved', person.pk)

def user_crawling(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    sc(person)
    return JsonResponse({})


@login_required
def index(request):
    form = AlgorithmFrom
    User = get_user_model()
    users = User.objects.all()
    algo = request.user.user_algotithms.filter(created_at__gt=datetime.date.today())
    today = datetime.date.today()
    users_inpo = []
    for user in users:
        algo = user.user_algotithms.filter(created_at__gt=datetime.date.today())
        if algo:
            problem = algo[0].problem
        else:
            problem = None
        users_inpo.append({'user':user,'problem':problem})
    context = {
        'users_inpo' : users_inpo,
    }
    return render(request, 'algorithms/index.html',context)


def create(request):
    problem = get_object_or_404(Problem, problem_num = int(request.POST.get('problem_num')))
    algorithm = Algorithm()
    algorithm.problem = problem
    algorithm.user = request.user
    algorithm.save()
    return redirect('algorithms:index')
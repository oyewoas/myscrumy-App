from ayooluwaoyewoscrumy.models import GoalStatus, ScrumyGoals, ScrumyHistory
from django.contrib.auth.models import User, Group, Permission
from .models import SignUpForm, CreateGoalForm, AddGoalForm, WeekOnlyAddGoalForm, QAChangegoal, DevMoveGoalForm, AdminChangeGoalForm, QAChangeGoalForm
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from random import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .models import ScrumyGoals, GoalStatus

content_type_scrumygoals = ContentType.objects.get_for_model(ScrumyGoals)
content_type_goalstatus = ContentType.objects.get_for_model(GoalStatus)

developergroup = Group.objects.get(name='Developer')
admingroup = Group.objects.get(name='Admin')
qualityassurancegroup = Group.objects.get(name='Quality Assurance')
ownergroup = Group.objects.get(name='Owner')
verifygoal = GoalStatus.objects.get(status_name="Verify Goal")


# permission_can_create_a_new_weekly_goal_for_himself_alone = Permission.objects.create(codename='can_create_weekly_goal_for_himself_alone',
# name='Can Create Weekly Goal For Himself Alone',content_type=content_type_scrumygoals)
# developergroup.permissions.add(permission_can_create_a_new_weekly_goal_for_himself_alone)
# qualityassurancegroup.permissions.add(permission_can_create_a_new_weekly_goal_for_himself_alone)

# permission_can_create_a_new_weekly_goal = Permission.objects.create(codename='can_create_new_weekly_goal',
# name='Can Create Weekly Goal',content_type=content_type_scrumygoals)
# ownergroup.permissions.add(permission_can_create_a_new_weekly_goal)

# permission_can_move_from_weeklygoal_to_dailygoal_and_verifygoal = Permission.objects.create(codename = 'can_move_from_weeklygoal_to_dailygoal_and_verifygoal',
# name='Can move from weeklygoal to dailygoal and verifygoal', content_type=content_type_goalstatus)
# developergroup.permissions.add(permission_can_move_from_weeklygoal_to_dailygoal_and_verifygoal)

# permission_can_move_goals_to_any_other_goalstatus = Permission.objects.create(codename = 'can_move_goals_to_any_other_goalstatus',
# name='Can move goals to any other goalstatus', content_type=content_type_goalstatus)
# qualityassurancegroup.permissions.add(permission_can_move_goals_to_any_other_goalstatus)

# permission_can_move_anybodys_goal_from_verifygoal_to_donegoal = Permission.objects.create(codename = 'can_move_anybodys_goal_from_verifygoal_to_donegoal',
# name='Can move anybodys goal from verifygoal to done goal', content_type=content_type_goalstatus)
# qualityassurancegroup.permissions.add(permission_can_move_anybodys_goal_from_verifygoal_to_donegoal)

# permission_can_move_anybodys_goal_to_any_of_the_goalstatus = Permission.objects.create(codename = 'can_move_anybodys_goal_to_any_of_the_goalstatus',
# name='Can move anybodys goal to any of the goal status', content_type=content_type_goalstatus)
# admingroup.permissions.add(permission_can_move_anybodys_goal_to_any_of_the_goalstatus)

# permission_can_move_his_goals_anywhere = Permission.objects.create(codename = 'can_move_his_goals_anywhere',
# name='Can move his goals anywhere', content_type=content_type_goalstatus)
# ownergroup.permissions.add(permission_can_move_his_goals_anywhere)

def index(request):
    form = SignUpForm()
    if request.method == 'GET':
        return render(request, 'ayooluwaoyewoscrumy/index.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            formdata = request.POST.copy()
            username = formdata.get('username')
            form.save()
            devgroupuser = Group.objects.get(name='Developer')
            user = User.objects.get(username=username)
            devgroupuser.user_set.add(user)
            successful = 'Your account has been created successfully'
            context = {'success': successful}
            return render(request, 'ayooluwaoyewoscrumy/successful.html', context)
    else:
        form = SignUpForm()
        return HttpResponseRedirect(reverse('ayooluwaoyewoscrumyindex:index'))


def scrumygoals(request):
    response = ScrumyGoals.objects.all()
    return HttpResponse(response)


def specificgoal(request):
    response = ScrumyGoals.objects.filter(goal_name='Learn Django')
    return HttpResponse(response)


# def move_goals(request, goal_id):
#     if not request.user.is_authenticated:
#         return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#     form = DevMoveGoalForm()
#     user = request.user
#     try:
#         goal = ScrumyGoals.objects.get(pk=goal_id)
#     except ObjectDoesNotExist:
#         notexist = 'A record with that goal id does not exist'
#         context = {'not_exist': notexist}
#         return render(request, 'ayooluwaoyewoscrumy/exception.html', context)
#     if request.method == 'GET':
#         return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal})
#     elif request.method == 'POST':
#         form = DevMoveGoalForm(request.POST, instance=goal)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
#     else:
#         form = DevMoveGoalForm()
#         return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal})


def move_goals(request, goal_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    # goals = get_object_or_404(ScrumyGoals, pk=goal_id)
    try:
        goal = ScrumyGoals.objects.get(pk=goal_id)
    except ObjectDoesNotExist:
        notexist = 'A record with that goal id does not exist'
        context = {'not_exist': notexist}
        return render(request, 'ayooluwaoyewoscrumy/exception.html', context)
    if usr_grp == Group.objects.get(name='Developer') and current_user == goal.user:
        form = DevMoveGoalForm()

        if request.method == 'GET':
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

        if request.method == 'POST':
            form = DevMoveGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))

        else:
            form = DevMoveGoalForm()
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})

    if usr_grp == Group.objects.get(name='Developer') and current_user != goal.user:
        form = DevMoveGoalForm()

        if request.method == 'GET':
            notexist = 'Cannot move other users goals'
            context = {'not_exist': notexist}
            return render(request, 'ayooluwaoyewoscrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Admin'):
        form = AdminChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        else:
            form = AdminChangeGoalForm()
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    
    if usr_grp == Group.objects.get(name='Owner') and current_user == goal.user:
        form = AdminChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        else:
            form = AdminChangeGoalForm()
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    else:
        notexist = 'You cannot move other users goals'
        context = {'not_exist': notexist}
        return render(request, 'ayooluwaoyewoscrumy/exception.html', context)
    
    
    if usr_grp == Group.objects.get(name='Quality Assurance') and current_user == goal.user:
        form = QAChangegoal()

        if request.method == 'GET':
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = QAChangegoal(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        else:
            form = QAChangegoal()
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

    if usr_grp == Group.objects.get(name='Quality Assurance') and current_user != goal.user and goal.goal_status == verifygoal:
        form = QAChangeGoalForm()
        if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
                form = QAChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))

        else:
                form = QAChangeGoalForm()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
    else: 
        notexist = 'You can only move goal from verify goals to done goals'
        context = {'not_exist': notexist}
        return render(request, 'ayooluwaoyewoscrumy/exception.html', context)


def add_goal(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = CreateGoalForm()
    if request.method == 'GET':
        return render(request, 'ayooluwaoyewoscrumy/addgoal.html', {'form': form})
    elif request.method == 'POST':
        form = CreateGoalForm(request.POST)
        post = form.save(commit=False)
        goal_id = randint(1000, 9999)
        status_name = GoalStatus(id=1)
        post.created_by = "Louis"
        post.moved_by = "Louis"
        post.owner = "Louis"
        post.goal_id = goal_id
        post.goal_status = status_name
        post.save()
    else:
        form = CreateGoalForm()
    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:addgoal'))


def home(request):
    scrumygoal = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    output = ', '.join([eachgoal.goal_name for eachgoal in scrumygoal])
    return HttpResponse(output)


def homepage(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = User.objects.all()
    current_user = request.user
    group = current_user.groups.values_list('name', flat=True)[0]
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    wg = weeklygoal.scrumygoals_set.all()
    dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
    dg = dailygoal.scrumygoals_set.all()
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    vg = verifygoal.scrumygoals_set.all()
    donegoal = GoalStatus.objects.get(status_name="Done Goal")
    gd = donegoal.scrumygoals_set.all()

    if current_user.is_authenticated:
        if group == 'Developer' or group == 'Owner' or group == 'Quality Assurance':
            form = WeekOnlyAddGoalForm()
            context = {'user': user, 'weeklygoal': wg, 'dailygoal': dg, 'verifygoal': vg,
                       'donegoal': gd, 'form': form, 'currentuser': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/home.html', context)
            if request.method == 'POST':
                form = WeekOnlyAddGoalForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    goal_id = randint(1000, 9999)
                    post.moved_by = current_user.first_name
                    post.owner = current_user.first_name
                    post.goal_id = goal_id
                    post.goal_status = weeklygoal
                    post.user = current_user
                    post.save()

            else:
                form = WeekOnlyAddGoalForm()
            return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        if group == 'Admin':
            context = {'user': user, 'weeklygoal': wg, 'dailygoal': dg, 'verifygoal': vg,
                       'donegoal': gd, 'currentuser': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/home.html', context)
            
               

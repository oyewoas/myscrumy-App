from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class GoalStatus(models.Model):
    status_name = models.CharField(max_length=200)
    def __str__(self):
        return self.status_name


class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=200)
    goal_id = models.AutoField(primary_key=True)
    created_by = models.CharField(max_length=200)
    moved_by =  models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    def __str__(self):
        return self.goal_name
    
        
class ScrumyHistory(models.Model):
    moved_by =  models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200)
    moved_to = models.CharField(max_length=200)
    time_of_action = models.TimeField('time of action')
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.CASCADE)
    def __str__(self):
        return self.moved_by

# Add more fields to user table
fullname = models.CharField(max_length=500, name='fullname', blank=True)
fullname.contribute_to_class(User, 'fullname')
usertype = models.CharField(max_length=30, blank=True)
usertype.contribute_to_class(User, 'usertype')

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user']

class AddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'goal_status']

class WeekOnlyAddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']
# class MoveGoalForm(ModelForm):
#     class Meta:
#         model = ScrumyGoals
#         fields = ['goal_status']

class DevMoveGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class OwnerChangeGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']
class AdminOthersChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QADoneChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class QAPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class QAVerifyChangegoal(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:2][::-1]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']
# class QAChangeGoalForm(ModelForm):
#     class Meta:
#         model = ScrumyGoals
#         fields = ['goal_status', 'user']

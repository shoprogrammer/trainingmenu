from django.shortcuts import render,redirect,get_object_or_404
from .forms import TrainingForm,SubTrainingForm,MainTrainingForm,AuxiliaryForm
from .models import TrainingModel,SubTrainingModel,MainTrainingModel,Auxiliary
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
import math
from django.db.models import Sum,F
from django.db.models import Count
from django.db import models

def listtraining(request):
    template_name = 'training/list-training.html'
    trainings = TrainingModel.objects.all().order_by('-created_at')
    #profileの情報取得test
    
    user = request.user
    if user.id:
        profile = Profile.objects.get(user=user)
    else:
        profile = "ゲスト"
    #test related
    # subtrainings = SubTrainingModel.objects.get(training_id=17,pk=16)

    trainings = TrainingModel.objects.prefetch_related('maintrainings','subtrainings').annotate(
                                                                        main_total_weight = Sum('maintrainings__total_weight'),
                                                                        sub_total_weight = Sum('subtrainings__total_weight'),
                                                                        total_total_weight = F('main_total_weight') + F('sub_total_weight'),
                                    ).order_by('-created_at')

    return render(request,template_name,{"trainings":trainings,"profile":profile})

def newtraining(request):
    template_name = 'training/new-training.html'
    form = TrainingForm()
    return render(request,template_name,{'form':form})

@login_required
def createtraining(request):
    template_name = 'training/new-training.html'
    
    if request.POST:
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('list-training')
    else:
        form = TrainingForm()
    return render(request,template_name,{'form':form})
    
def detailtraining(request,pk):
    template_name = 'training/detail-training.html'
    training = TrainingModel.objects.get(pk=pk)

    subtrainings = SubTrainingModel.objects.filter(training_id=pk)
    maintrainings = MainTrainingModel.objects.filter(training_id=pk)


    #サブトレ合計重量 重量✖️セット数✖️レップ数
    weight_subtraining = subtrainings.aggregate(weight_subtraining=Sum('total_weight'))
    weight_subtraining = weight_subtraining['weight_subtraining'] 
    if weight_subtraining == None:
        weight_subtraining = 0

    
    #メイントレ合計重量 
    weight_maintraining = maintrainings.aggregate(weight_maintraining=Sum('total_weight'))
    weight_maintraining = weight_maintraining['weight_maintraining'] 
    if weight_maintraining == None:
        weight_maintraining = 0

 
    weight_total = int(weight_subtraining) + int(weight_maintraining)

    return render(request,template_name,{'training':training,'subtrainings':subtrainings,'maintrainings':maintrainings,
                                         'weight_subtraining':weight_subtraining,'weight_maintraining':weight_maintraining,
                                         'weight_total':weight_total})


def edittraining(request,pk):
    template_name = 'training/edit-training.html'
    training = TrainingModel.objects.get(pk=pk)
    form = TrainingForm(instance=training)
    return render(request,template_name,{'training':training,'form':form})


def updatetraining(request,pk):
    template_name = 'training/edit-training.html'
    
    training = TrainingModel.objects.get(pk=pk)
    if request.POST:
        form = TrainingForm(request.POST,instance=training)
        if form.is_valid():
            form.save()
            print(1)
            return redirect('list-training')
    else:
        form = TrainingForm(instance=training)
    return render(request,template_name,{"form":form,"training":training})



def deletetraining(request,pk):
    training = TrainingModel(pk=pk)
    if request.POST:
        training.delete()
        return redirect('list-training')
    return redirect('list-training')


@login_required
def my_training(request):
    template_name = 'mytraining/my-training.html'
    user = request.user
    trainings = user.trainings.all().order_by("-created_at")


    trainings = user.trainings.prefetch_related('maintrainings','subtrainings').annotate(
                                                                        main_total_weight = Sum('maintrainings__total_weight'),
                                                                        sub_total_weight = Sum('subtrainings__total_weight'),
                                                                        total_total_weight = F('main_total_weight') + F('sub_total_weight'),
                                    ).order_by('-created_at')
    weight_totaltraining = trainings.aggregate(weight_totaltraining=Sum('total_total_weight'))
    weight_totaltraining = weight_totaltraining['weight_totaltraining']
    if weight_totaltraining == None:
        weight_totaltraining = 0

    return render(request,template_name,{'trainings':trainings,'weight_totaltraining':weight_totaltraining})

#subtraining
def newsubtraining(request,pk):
    template_name = 'subtraining/new-subtraining.html'
  
    form = SubTrainingForm()
    # form.instance.user = request.user
    # form.instance.training_id=pk
    training = TrainingModel.objects.get(pk=pk)
    return render(request,template_name,{'form':form,"training":training})












def createsubtraining(request,pk):
    template_name = 'subtraining/new-subtraining.html'
    training = get_object_or_404(TrainingModel, pk=pk)
    if request.POST:
        form = SubTrainingForm(request.POST)
        print(training.pk)
        print(training.id)
        if form.is_valid():
            form.instance.user =request.user
            #koko
            form.instance.training = training
            form.save()
            return redirect('detail-training',pk=pk)
    else:
        form = SubTrainingForm()

    return render(request,template_name,{'form':form,'training':training})


def detailsubtraining(request,training_pk,subtraining_pk):
    template_name = 'subtraining/detail-subtraining.html'
    training = TrainingModel.objects.get(pk=training_pk)
    subtraining = SubTrainingModel.objects.get(training_id=training_pk,pk=subtraining_pk)
    return render(request,template_name,{"subtraining":subtraining,"training":training})



def editsubtraining(request,training_pk,subtraining_pk):
    template_name = 'subtraining/edit-subtraining.html'
    training = TrainingModel.objects.get(pk=training_pk)
    subtraining = SubTrainingModel.objects.get(training_id=training_pk,pk=subtraining_pk)   
    form = SubTrainingForm(instance=subtraining)
    return render(request,template_name,{'subtraining':subtraining,'form':form,'training':training})





def updatesubtraining(request,training_pk,subtraining_pk):
    template_name = 'subtraining/edit-subtraining.html'
    subtraining = SubTrainingModel.objects.get(training_id = training_pk,pk=subtraining_pk)
    if request.POST:
        form = SubTrainingForm(request.POST,instance=subtraining)
        if form.is_valid():
            form.save()
            return redirect('detail-training',pk=training_pk)
    return render(request,template_name,{"form":form,"subtraining":subtraining})

def deletesubtraining(request,training_pk,subtraining_pk):
    subtraining = SubTrainingModel(training_id=training_pk,pk=subtraining_pk)
    if request.POST:
        subtraining.delete()
        return redirect('detail-training',pk=training_pk)
    return redirect('detail-training',pk=training_pk)







#maintraining
def displaymaintraining(request,pk):
    template_name = 'maintraining/display-maintraining.html'
    training = TrainingModel.objects.get(pk=pk)
    maintraining = MainTrainingModel.objects.get(pk=pk)
    return render(request,template_name,{"training":training,"maintraining":maintraining})


def detailmaintraining(request,training_pk,maintraining_pk):
    template_name = 'maintraining/detail-maintraining.html'
    training = TrainingModel.objects.get(pk=training_pk)
    maintraining = MainTrainingModel.objects.get(training_id=training_pk,pk=maintraining_pk)
    return render(request,template_name,{'training':training,'maintraining':maintraining})




def newmaintraining(request,pk):
    template_name='maintraining/new-maintraining.html'
    form = MainTrainingForm()
    training = TrainingModel.objects.get(pk=pk)

    return render(request,template_name,{'form':form,'training':training})






def createmaintraining(request,pk):
    template_name = 'maintraining/new-maintraining.html'
    training = get_object_or_404(TrainingModel,pk=pk)
    if request.POST:
        form = MainTrainingForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.training = training
            form.save()
            return redirect('detail-training',pk=pk)
    else:
        form = MainTrainingForm()

    return render(request,template_name,{'form':form,'training':training})


def updatemaintraining(request,training_pk,maintraining_pk):
    template_name = 'maintraining/edit-maintraining.html'
    maintraining = MainTrainingModel.objects.get(training_id = training_pk,pk=maintraining_pk)
    if request.POST:
        form = MainTrainingForm(request.POST,instance=maintraining)
        if form.is_valid():
            form.save()
            return redirect('detail-training',pk=training_pk)
    return render(request,template_name,{'form':form,'maintraining':maintraining})









def editmaintraining(request,training_pk,maintraining_pk):
    template_name = 'maintraining/edit-maintraining.html'
    training = TrainingModel.objects.get(pk=training_pk)
    maintraining = MainTrainingModel.objects.get(training_id=training_pk,pk=maintraining_pk)
    form = MainTrainingForm(instance=maintraining)
    return render(request,template_name,{'maintraining':maintraining,'training':training,'form':form})



def deletemaintraining(request,training_pk,maintraining_pk):
    maintraining = MainTrainingModel(training_id=training_pk,pk=maintraining_pk)
   
  

    if request.POST:
        if request.POST.get('delete'):
            action = request.POST.get('delete')
            if action == "1":
                print("削除しますた")
                maintraining.delete()
        return redirect('detail-training',pk=training_pk)
    return redirect('detail-training',pk=training_pk)                    

@login_required
def newipfpoint(request):
    template_name = "ipf/ipf.html"
    user = request.user
    profile = Profile.objects.get(user=user)


             #   """GLポイントを計算する関数"""
    if profile.gender == 'm':
        a, b, c  = 1199.72839, 1025.18162, -0.00921
    elif profile.gender == 'f':
        a, b, c= 610.32796, 1045.59282, -0.03048

    weight = int(profile.weight)

    denominator = (a 
                   - b ** 
                   (c* weight)
                   
                   )
    print(denominator)         

    gl_point = (100 * profile.total_score) / denominator

    print(gl_point)
    return render(request,template_name,{"profile":profile,"gl_point":gl_point})



def totalscore(request):
    template_name = "totalscore/totalscore.html"
    user = request.user
    
    if "gender" not in request.session:
        request.session["gender"] = "m"
    
    gender = request.session["gender"]
    profiles = Profile.objects.filter(gender=gender).order_by('-total_score')
    

  
    return render(request,template_name,{"user":user,"profiles":profiles})


def switchtotalscore(request):
    template_name = "totalscore/totalscore.html"
    
    current_gender = request.session.get('gender','m')

    if current_gender == 'm':
        new_gender = 'f'
    else:
        new_gender = 'm'

    request.session['gender'] = new_gender

    profiles = Profile.objects.filter(gender=new_gender).order_by('-total_score')

    
    return render(request,template_name,{"profiles":profiles,"new_gender":new_gender})


def glpoints(request):
    template_name = "glpoints/glpoints.html"
    user = request.user
    profiles = Profile.objects.all().order_by('-gl_point')

    return render(request,template_name,{"user":user,"profiles":profiles})



def add_auxiliary(request,training_pk,subtraining_pk):


    if request.method == "POST" :
        form = AuxiliaryForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.training = TrainingModel.objects.get(pk=training_pk)
            form.instance.subtraining = SubTrainingModel.objects.get(pk=subtraining_pk,training_id=training_pk)
            form.save()
            return redirect('detail-training',pk=training_pk)
    return redirect('detail-training',pk=training_pk)

def remove_auxiliary(request,training_pk,subtraining_pk):
    training = TrainingModel.objects.get(pk=training_pk)
    subtraining = SubTrainingModel.objects.get(training_id=training_pk,subtraining_pk=subtraining_pk)
    if request.POST:
        auxiliary = Auxiliary.objects.get(user=request.user,training=training,subtraining=subtraining)
        auxiliary.delete()
        return redirect('detail-training')
    return redirect('detail-training')


#rmlist
def rmlist(request):
    template_name = 'rm/rmlist.html'
    return render(request,template_name)



#折れ線グラフ作成
def linegrah(request):
    template_name = "linegraph/linegraph.html"

    #総負荷重量データ
    user = request.user
    trainings = user.trainings.all().order_by("date")


    trainings = user.trainings.prefetch_related('maintrainings','subtrainings').annotate(
                                                                        main_total_weight = Sum('maintrainings__total_weight'),
                                                                        sub_total_weight = Sum('subtrainings__total_weight'),
                                                                        total_total_weight = F('main_total_weight') + F('sub_total_weight'),
                                    ).order_by('date')
    
    dates =[]
    total_weights = []
    maintotal_weights = []
    subtotal_weights = []
    for training in trainings:
        date = training.date.strftime('%Y-%m-%d')
        total_weight = training.total_total_weight
        maintotal_weight = training.main_total_weight 
        subtotal_weight = training.sub_total_weight 
        if training.total_total_weight == None:
            total_weight = 0
        if training.main_total_weight == None:
            maintotal_weight = 0
        if training.sub_total_weight == None:
            subtotal_weight = 0

        dates.append(date)
        total_weights.append(total_weight)
        maintotal_weights.append(maintotal_weight)
        subtotal_weights.append(subtotal_weight)

        





    #全体のweight----------------------
    weight_totaltraining = trainings.aggregate(weight_totaltraining=Sum('total_total_weight'))
    weight_totaltraining = weight_totaltraining['weight_totaltraining']
    if weight_totaltraining == None:
        weight_totaltraining = 0
    #---------------------------------


    context={"weight_totaltraining":weight_totaltraining,
             "total_weights":total_weights,
             "maintotal_weights":maintotal_weights,
             "subtotal_weights":subtotal_weights,
             "dates":dates,
             
             
             }
    
    return render(request,template_name,context)

def program(request):
    template_name="program/program.html"
    
    return render(request,template_name)
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.listtraining,name='list-training'),
    path('newtraining/',views.newtraining,name='new-training'),
    path('createtraining/',views.createtraining,name='create-training'),
    path('deletetraining/<int:pk>/',views.deletetraining,name='delete-training'),
    path('detailtraining/<int:pk>/',views.detailtraining,name='detail-training'),
    path('edittraining/<int:pk>/',views.edittraining,name='edit-training'),
    path('updatetraining/<int:pk>/',views.updatetraining,name='update-training'),

    #自分のメニュ
    path('my_training/',views.my_training,name='my_training'),

    #サブメニュ
    path('newsubtraining/<int:pk>/',views.newsubtraining,name='new-subtraining'),
    path('createsubtraining/<int:pk>/',views.createsubtraining,name='create-subtraining'),
    path('detailsubtraining/<int:training_pk>/detail/<int:subtraining_pk>/',views.detailsubtraining,name='detail-subtraining'),
    path('editsubtraining/<int:training_pk>/edit/<int:subtraining_pk>/',views.editsubtraining,name='edit-subtraining'),
    path('updatesubtraining/<int:training_pk>/update/<int:subtraining_pk>/',views.updatesubtraining,name='update-subtraining'),
    path('deletesubtraining/<int:training_pk>/delete/<int:subtraining_pk>/',views.deletesubtraining,name='delete-subtraining'),

    #メインメニュ
    path('newmaintraining/<int:pk>/',views.newmaintraining,name='new-maintraining'),
    path('createmaintraining/<int:pk>/',views.createmaintraining,name='create-maintraining'),
    path('detailmaintraining/<int:training_pk>/detail/<int:maintraining_pk>/',views.detailmaintraining,name='detail-maintraining'),
    path('updatemaintraining/<int:training_pk>/update/<int:maintraining_pk>/',views.updatemaintraining,name='update-maintraining'),
    path('editmaintraining/<int:training_pk>/edit/<int:maintraining_pk>/',views.editmaintraining,name='edit-maintraining'),
    path('deletetraining/<int:training_pk>/delete/<int:maintraining_pk>/',views.deletemaintraining,name='delete-maintraining'),

    #IPF求める
    path('newipfpoint/',views.newipfpoint,name='new-ipfpoint'),

    #totalscoreを求める
    path('total_score/',views.totalscore,name='total-score'),

    #totalscoreを男、女でswitch
    path('switchtotalscore/',views.switchtotalscore,name='switch-totalscore'),

    #GLpoint
    path('glpoints/',views.glpoints,name='gl-points'),

    #補助トレsub用
    path('add_auxiliary/<int:training_pk>/add/<int:subtraining_pk>/',views.add_auxiliary,name='add-auxiliary'),
    path('remove_auxiliary/<int:training_pk>/remove/<int:subtraining_pk>/',views.remove_auxiliary,name='remove-auxiliary'),

    #RM一覧
    path('rmlist/',views.rmlist,name='rm-list'),

    #折れ線グラフ
    path("linegraph/",views.linegrah,name='line-graph'),

    #program一覧
    path('program/',views.program,name='program'),

     
]
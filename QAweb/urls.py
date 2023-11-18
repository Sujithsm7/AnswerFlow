from django.contrib import admin
from django.urls import path
from QAweb import views





urlpatterns = [
    path("register",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index",views.IndexView.as_view(),name="index"),
    path("questions/<int:id>/answers/add",views.add_answer,name="add-answer"),
    path('answers/<int:id>/upvotes/add',views.answer_upvote_view,name="add-upvote"),
    path("logout",views.signout_view,name="sign-out")
]

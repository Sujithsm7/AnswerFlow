from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView
from QAweb.forms import UserRegistrationForm,LoginForm,QuestionForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib import messages
from api.models import Questions,Answers
from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect('signin')
        else:
            return fn(request,*args,**kw)
    return wrapper

#####



decs=[signin_required,never_cache] #


######

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")


class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,"login.html",{"form":form})
            

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    success_url=reverse_lazy("index")
    model=Questions
    context_object_name="questions"

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"your question added successfully")   #save akkunnathinu munpe extra activity cheyyan
        return super().form_valid(form)
    
    def  get_queryset(self):
        return Questions.objects.exclude(user=self.request.user).order_by("-createddate") #login cheythavarude ozhike bakki ellam list akkan


######answer add akkan
@signin_required
@never_cache
def add_answer(request,*args,**kw):
    id=kw.get("id")
    ques=Questions.objects.get(id=id)
    ans=request.POST.get("Answer")
    Answers.objects.create(question=ques,
                           answer=ans,
                           user=request.user)
    messages.success(request,"Your answer posted successfully")
    return redirect("index")


####upvote view
@signin_required
@never_cache
def answer_upvote_view(request,*args,**kw):
    id=kw.get("id")
    ans=Answers.objects.get(id=id)
    ans.upvote.add(request.user)
    return redirect("index")


##logout
@signin_required
@never_cache
def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")
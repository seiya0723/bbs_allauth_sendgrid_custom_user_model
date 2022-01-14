from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Topic
from .forms import TopicForm

class IndexView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        context = {}
        context["topics"]   = Topic.objects.all()

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = TopicForm(copied)

        if not form.is_valid():
            print("バリデーションNG")
            return redirect("bbs:index")
        
        print("バリデーションOK")
        form.save()

        return redirect("bbs:index")

index   = IndexView.as_view()


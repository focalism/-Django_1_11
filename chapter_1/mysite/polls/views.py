# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.http import Http404

def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list':latest_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})
def results(request,question_id):
    response = "You're looking at the result  of question %s"
    return HttpResponse(response %question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新打印“问题”投票表单
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 您在处理完 POST 数据后请使用 HttpResponseRedirect 跳转页面，通过这种方式
        # 可以防止用户不小心点击后退按钮后重复提交表单
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    

# Create your views here.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five publish question."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DeleteView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DeleteView):
    model = Question
    template_name = 'polls/results.html'

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

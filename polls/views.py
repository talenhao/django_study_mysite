from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic


# def index(request):
#     return HttpResponse('Hello world. You are in the Polls index.')

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[0:5]
#     # output = ','.join([q.question_text for q in latest_question_list])
#     tempalte = loader.get_template('polls/index.html')
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     # return HttpResponse(tempalte.render(context, request))
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    '''
    默认使用 <app name>/<model name>_list.html，使用tempate_name修改默认模板
    默认使用<model name>_list定义model,使用context_object_name修改默认
    '''
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return the late five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist.")
#     return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse("You're look at question %s." % question_id)


class DetailView(generic.DetailView):
    '''
    默认使用 <app name>/<model name>_detail.html，使用tempate_name手工指定模板.
    '''
    model = Question
    template_name = 'polls/detail.html'


def vote(request, question_id):
    # 生成实例
    question = get_object_or_404(Question, pk=question_id)
    # 取出提交上来的choice
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # 重新显示提交表单
        render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 跳转到结果界面
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question": question})
#

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


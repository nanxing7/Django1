from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, question_id):
    """
    结果展示页面
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You didnt select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

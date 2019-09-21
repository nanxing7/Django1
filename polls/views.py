from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
# 导入 404 页面处理包
from django.http import Http404
# 导入快捷处理 404 函数
from django.shortcuts import get_object_or_404
from django.urls import reverse


# def index(request):
#     """
#     展示数据库里以发布日期排序的最近5个投票问题
#     :param request:
#     :return:
#     """
#     # 利用 Django 自带的数据库功能查询排序发布日期的数据
#     latest_question_list = Question.objects.order_by('-pub_date'[:5])
#     # 定义 template 变量,载入 polls/index.html 模版文件
#     template = loader.get_template('polls/index.html')
#     # 定义上下文变量 context
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # 返回 Response 中 传入 template.render 方法, 并在 template.render 方法中传递一个上下文( context ),将模版内的变量映射为 python 对象
#     return HttpResponse(template.render(context, request))

def index(request):
    """
    [载入模版，填充上下文，再返回由它生成的 HttpResponse 对象] 是一个非常常用的操作流程，于是 Django 提供了一个快捷函数/封装了一个函数
    展示数据库里以发布日期排序的最近5个投票问题
    :param request:
    :return:
    """
    # 利用 Django 自带的数据库功能查询排序发布日期的数据
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 定义上下文变量 context ,并填充它
    context = {'latest_question_list': latest_question_list, }
    print(context, '\n', latest_question_list)
    # 利用 render 方法载入模版文件
    return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     """
#     投票详情视图 -- 会显示指定投票问题的标题
#     :param request:
#     :param question_id: 问题 id
#     :return:
#     """
#     # 异常处理如果指定问题的 id 所对应问题不存在，则该视图抛出 Http404 异常
#     try:
#         # 通过 Django 的数据库查询方法通过传入的 question_id 获取数据库对应的内容
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     context = {'question': question}
#     # 利用 render 方法载入模版文件
#     return render(request, 'polls/detail.html,', context)

def detail(request, question_id):
    """
    投票详情视图 -- 会显示指定投票问题的标题
    :param request:
    :param question_id: 问题 id
    :return:
    """
    # 用 Django 提供的快捷函数处理 404 错误，传入 Question 类，pk 为问题 id
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    # 利用 render 方法载入模版文件
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    """

    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


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

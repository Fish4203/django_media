from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class Index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('-date')

    additional_context = {'a':'polling', 'b':'index'}
    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        context['additional_context'] = self.additional_context
        print(context)
        return context


class Detail(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    additional_context = {'a':'polling'}
    def get_context_data(self, *args, **kwargs):
        context = super(Detail, self).get_context_data(*args, **kwargs)
        context['additional_context'] = self.additional_context
        print(context)
        return context

class Results(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    additional_context = {'a':'polling'}
    def get_context_data(self, *args, **kwargs):
        context = super(Results, self).get_context_data(*args, **kwargs)
        context['additional_context'] = self.additional_context
        #print(context)
        return context

def delete(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)

        if question.user == request.user:
            question.delete()
            return redirect('polls:index')
        else:
            return redirect('polls:index', error='could not authenticate')
    except:
        return redirect('polls:index', error='could not get question')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return redirect('polls:results', pk=question.id)

def new_question(request):
    if request.POST['question_name'] == '':
        return redirect('polls:index', error='question was blank')

    try:
        question = Question(user=request.user, question_text=request.POST['question_name'], date=timezone.now())
        question.save()
    except:
        return redirect('polls:index', error='could not create question')

    try:
        question.choice_set.create(choice_text=request.POST['option1'], votes=0)
        question.choice_set.create(choice_text=request.POST['option2'], votes=0)
        question.choice_set.create(choice_text=request.POST['option3'], votes=0)

        question.save()
    except:
        try:
            question.delete()

            return redirect('polls:index', error='could not create choices for question')
        except:
            return redirect('polls:index', error='could not create choices for question')


    return redirect('polls:index')


'''
    question_list = Question.objects.order_by('-date')
    input = {'question_list': question_list}

    return render(request, 'polls/index.html', input)



question = get_object_or_404(Question, pk=question_id)
return render(request, 'polls/results.html', {'question': question})
'''

from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView

from .forms import UserCreatingForm, UserLoginForm
from .models import Question, Choice
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class Register(generic.CreateView):
    template_name = 'polls/register.html'
    form_class = UserCreatingForm
    success_url = reverse_lazy('polls:login')


class Login(FormView):
    template_name = 'polls/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Аутентификация пользователя
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Неправильное имя пользователя или пароль.')
            return self.form_invalid(form)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

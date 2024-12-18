from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, UpdateView

from .forms import UserCreatingForm, UserLoginForm, UserUpdateForm
from .models import Question, Choice, User, Vote
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


def custom_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('polls:index')
    else:
        return redirect('polls:login')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class UserProfileListView(generic.ListView):
    model = User
    template_name = 'polls/profile.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'polls/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('polls:profile')


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


def question_list(request):
    questions = Question.objects.filter(is_active=True)
    return render(request, 'polls/question_list.html', {'questions': questions})


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if Vote.objects.filter(user=request.user, question=question).exists():
        return render(request, 'polls/already_voted.html', {'question': question})

    if request.method == "POST":
        choice_id = request.POST['choice']
        choice = get_object_or_404(Choice, pk=choice_id, question=question)

        Vote.objects.create(user=request.user, question=question, choice=choice)
        choice.votes += 1
        choice.save()

        total_votes = sum(choice.votes for choice in question.choice_set.all())
        results = [
            {
                'choice_text': c.choice_text,
                'votes': c.votes,
                'percentage': round((c.votes / total_votes) * 100, 2) if total_votes > 0 else 0
            }
            for c in question.choice_set.all()
        ]

        return render(request, 'polls/results.html', {'question': question, 'results': results})

    return render(request, 'polls/vote.html', {'question': question, 'choices': question.choice_set.all()})

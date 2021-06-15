from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .funtions import get_statistic
from .models import *
from .utils import DataMixin


def redirct(request):
    return redirect('home', permanent=False)


class GamesHome(DataMixin, ListView):
    model = Games
    template_name = 'games/home.html'
    context_object_name = 'games'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


class GamesCategory(DataMixin, ListView):
    model = Games
    template_name = 'games/home.html'
    context_object_name = 'games'
    allow_empty = False

    def get_queryset(self):
        return Games.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=str(c.name))
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'games/addpage.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


class ShowGame(DataMixin, DetailView):
    model = Games
    template_name = 'games/game_detail.html'
    slug_url_kwarg = 'slug_game'
    context_object_name = 'game'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['game'])
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'games/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'games/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'games/feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # print(form.cleaned_data)

        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    return HttpResponse('О нас страница')


class HandFormView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = HandForm
    template_name = 'games/bj_start.html'
    # success_url = reverse_lazy('bj_result')
    raise_exception = True

    def post(self, request, *args, **kwargs):
        # print(HandForm(request.POST))
        # print(request.__dict__)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Помощник BJ')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.played_by = self.request.user
        return super().form_valid(form)


class BjResult(LoginRequiredMixin, DataMixin, DetailView, UpdateView):
    form_class = HandFormUpdate
    model = Hand
    template_name = 'games/bj_result.html'
    context_object_name = 'hand'
    success_url = reverse_lazy('bj_start')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Помощник BJ')
        return dict(list(context.items()) + list(c_def.items()))


class HandStatistic(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 10
    model = Hand
    template_name = 'games/statistic.html'
    context_object_name = 'stats'
    allow_empty = False
    # hands = len(Hand.Hand.objects.filter(played_by='request.user.id'))
    # wins = len(Hand.Hand.objects.filter(played_by='request.user.id', win_result='win'))

    def get_queryset(self):
        return Hand.objects.filter(played_by=self.request.user.id).order_by('-time_hand')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['winreit'] = get_statistic(hands, wins)
        c_def = self.get_user_context(title='Статистика Пользователя')
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     cat = get_object_or_404(Category, slug=cat_slug)
#     games = Games.objects.filter(cat_id=cat.id)
#
#     context = {'menu': menu,
#                'title': 'Категория',
#                'games': games,
#                'categories': categories}
#
#     return render(request, 'games/home.html', context)


# def index(request):
#     games = Games.objects.all()
#
#     context = {'games': games,
#                'menu': menu,
#                'title': 'Все игры',
#                'categories': categories}
#
#     return render(request, 'games/home.html', context)


# def show_game(request, slug_game):
#     game = get_object_or_404(Games, slug=slug_game)
#     context = {'menu': menu,
#                'title': game.name,
#                'game': game,
#                'categories': categories}
#
#     return render(request, 'games/game_detail.html', context)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'games/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

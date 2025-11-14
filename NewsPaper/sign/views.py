from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import CreateView


from .forms import SignUpForm
from my_newspaper.models import Author


class SignUpView(CreateView):
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('user_profile')

def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')


@login_required
def user_profile(request):
    context = {
        'is_author': request.user.groups.filter(name='authors').exists(),
    }
    return render(request, 'sign/profile.html', context)

@login_required
def be_author(request):
    author = Author.objects.get_or_create(usr = request.user)
    group_authors = Group.objects.get(name = 'authors')
    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(group_authors)
    return redirect(request.META.get('HTTP_REFERER'))


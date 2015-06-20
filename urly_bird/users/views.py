from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from users.forms import UserForm, ProfileForm
from users.models import Profile
from bookmarks.models import Bookmark

# Create your views here.

class AddUserView(View):

    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, "register.html", {"form1": user_form, "form2": profile_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)

            login(self.request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Account Successfully Created.")
            return redirect("all_bookmarks")
        else:
            return render(request, "register.html", {"form1": user_form, "form2": profile_form})


class ShowUserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    # paginate_by = 20
    template_name = 'show_user.html'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmarks = Bookmark.objects.filter(user=self.object).order_by("-marked_at")
        user = self.request.user
        if user == self.object:
            own = True
        else:
            own = False
        context['bookmarks'] = bookmarks
        context['own'] = own
        return context


# class Index(View):
#     # paginate_by = 20
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

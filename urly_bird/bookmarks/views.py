from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView
from bookmarks.models import Bookmark, Click
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from bookmarks.forms import AddBookmarkForm
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy


# Create your views here.

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ShowBookmarkDetailView(DetailView):
    model = Bookmark
    context_object_name = 'bookmark'
    # paginate_by = 20
    template_name = 'show_bookmark.html'

    def get_object(self, queryset=None):
        return Bookmark.objects.get(pk=self.kwargs['bm_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicks = Click.objects.filter(bookmark=self.object)
        context['clicks'] = clicks
        return context


class AllBookmarksView(ListView):
    model = Bookmark
    context_object_name = 'all_bookmarks'
    queryset = Bookmark.objects.all().order_by('-marked_at')
    # paginate_by = 20
    template_name = 'all_bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddBookmarkView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        form = AddBookmarkForm(initial={'user': self.request.user})
        return render(request, "new_bookmark.html", {"form": form})

    def post(self, request, **kwargs):
        form = AddBookmarkForm(request.POST, initial={'user': self.request.user})
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.marked_at = timezone.now()
            bookmark.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your bookmark was successfully created!")
            return redirect("/b/")
        else:
            return render(request, "new_bookmark.html", {"form": form})


class BookmarkUpdate(LoginRequiredMixin, UpdateView):
    model = Bookmark
    form_class = AddBookmarkForm
    template_name = 'bookmark_update_form.html'

    def get_success_url(self):
        return reverse('show_bookmark', kwargs={'bm_id': self.kwargs['bm_id']})

    def get_object(self, queryset=None, **kwargs):
        bookmark = Bookmark.objects.get(id=self.kwargs['bm_id'])
        return bookmark

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your bookmark was successfully updated!")
        return super(BookmarkUpdate, self).form_valid(form)


class BookmarkDelete(LoginRequiredMixin, DeleteView):
    model = Bookmark

    def get_success_url(self):
        return reverse_lazy('show_user', kwargs={'user_id': self.request.user.id})

    def get_object(self, queryset=None):
        return Bookmark.objects.filter(pk=self.kwargs['bm_id'])

    def get_template_names(self):
        return 'bookmark_confirm_delete.html'

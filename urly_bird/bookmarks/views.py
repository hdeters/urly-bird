from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView, RedirectView
from bookmarks.models import Bookmark, Click, Tag
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from bookmarks.forms import AddBookmarkForm
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from hashids import Hashids
from django.http import HttpResponseRedirect, HttpResponse


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
        clicks = Click.objects.filter(bookmark=self.object).order_by("-time")
        context['clicks'] = clicks
        return context


class AllBookmarksView(ListView):
    model = Bookmark
    context_object_name = 'all_bookmarks'
    queryset = Bookmark.objects.all().select_related().order_by('-marked_at')
    paginate_by = 20
    template_name = 'all_bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class AddBookmarkView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        form = AddBookmarkForm(initial={'user': self.request.user})
        return render(request, "new_bookmark.html", {"form": form})

    def post(self, request, **kwargs):
        hashids = Hashids(salt='saltstring')
        form = AddBookmarkForm(request.POST, initial={'user': self.request.user})
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.marked_at = timezone.now()
            bookmark.save()
            hash = hashids.encode(bookmark.id)
            bookmark.hash_id = hash
            bookmark.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your bookmark was successfully created!")
            return redirect("/b/")
        else:
            return render(request, "new_bookmark.html", {"form": form})


class TagListView(ListView):
    model = Bookmark
    context_object_name = 'top_in_tag'
    paginate_by = 20
    template_name = 'tag_list.html'

    def get_queryset(self):
        the_tag = Tag.objects.get(pk=self.kwargs['tag_id'])
        return Bookmark.objects.filter(tags=the_tag).order_by('-marked_at')

    def get_context_data(self, **kwargs):
        the_tag = Tag.objects.get(pk=self.kwargs['tag_id'])
        context = super().get_context_data(**kwargs)
        context["tag"] = the_tag.name
        return context


class ShowSite(View):
    def get(self, request, **kwargs):
        hashids = Hashids(salt='saltstring')
        id = hashids.decode(kwargs['url'])[0]
        bookmark = Bookmark.objects.get(pk=id)
        new_url = bookmark.url
        if request.user.is_authenticated():
            click = Click(user_id=request.user, bookmark=bookmark, time=timezone.now())
            click.save()
        else:
            user = User.objects.filter(username='Anonymous')[0]
            click = Click(user_id=user, bookmark=bookmark, time=timezone.now())
            click.save()
        return HttpResponseRedirect(new_url)


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


from django.forms import model_to_dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.style.use('ggplot')
from matplotlib.dates import DateFormatter

def click_chart(request):
    clicks = Click.objects.all()
    df = pd.DataFrame(model_to_dict(click) for click in clicks)
    df['count'] = 1
    df.index = df['time']
    counts = df['count']
    counts = counts.sort_index()
    series = pd.expanding_count(counts).resample('W', how=np.max, fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(series)
    series.plot()
    plt.title("Total clicks over time")
    plt.xlabel("")
    canvas = FigureCanvas(fig)
    canvas.print_png(response)
    return response

def link_chart(request, bm_id):
    bookmark = Bookmark.objects.get(pk=bm_id)
    clicks = Click.objects.filter(bookmark=bookmark)
    df = pd.DataFrame(model_to_dict(click) for click in clicks)
    df['count'] = 1
    df.index = df['time']
    counts = df['count']
    counts = counts.sort_index()
    response = HttpResponse(content_type='image/png')

    if bookmark.marked_at > (timezone.now() - timezone.timedelta(days=2)):
        series = df.resample('H', how={'count': 'count'})
        recent_data = series
        #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(recent_data)
        fig.autofmt_xdate()
        #recent_data.plot()
        plt.title("Number of Clicks Per Hour")
        plt.xlabel("Past 24 Hours")
        canvas = FigureCanvas(fig)
        canvas.print_png(response)
        return response
    else:
        series = df.resample('D', how={'count': 'count'})
        recent_data = series[-30:]
        #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(recent_data)
        fig.autofmt_xdate()
        #recent_data.plot()
        plt.title("Number of Clicks Per Day")
        plt.xlabel("Last 30 Days")
        canvas = FigureCanvas(fig)
        canvas.print_png(response)
        return response


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post


def home(Request):
    context={
        'posts': Post.objects.all()
    }
    return render(Request, 'requests/home.html', context)

class PostListView(ListView):
    model= Post
    template_name='requests/home.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']

class PostDetailView(DetailView):
    model= Post

#class based view for creating post
#redirects to login page if attempted access without being logged in
class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    fields=['title', 'category', 'status', 'content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

#class based view to update post
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Post
    fields=['title', 'category', 'status', 'content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(Request):
    return render(Request, 'requests/about.html', {'title': 'About'})

    
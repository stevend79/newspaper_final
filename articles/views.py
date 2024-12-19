# articles/views.py

from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Article, Comment
from .forms import CommentForm


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        # Redirect back to the same article page after submission
        return self.request.path

    def post(self, request, *args, **kwargs):
        # Ensure this method handles POST requests
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/article_new.html'
    fields = ['title', 'body']
    permission_required = 'articles.add_article'

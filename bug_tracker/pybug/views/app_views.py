from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from users.models import User
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from pybug.models import Ticket, Project, Comment
from pybug.forms import TicketForm, CommentForm


class ProjectlistView(ListView):
    model = Project
    template_name = 'pybug/projects.html'
    context_object_name = 'projects'
    ordering = ['-date_created']
    paginate_by = 10


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'key', 'description', 'lead']
    

class TicketListView(FormMixin, ListView):
    model = Ticket
    template_name = 'pybug/ticket_detail.html'
    context_object_name = 'tickets'
    paginate_by = 5
    form_class = TicketForm

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'instance': self.get_object()
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        ticket = self.get_object()
        return ticket.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket_form = self.get_form()

        if 'comment_content' in request.POST:
            comment_content = request.POST.get('comment_content')
            if comment_content != '':
                comment = Comment.objects.create(ticket=ticket, 
                                                    user=request.user, 
                                                    content=comment_content)
                comment.save()
        elif ticket_form.is_valid():
            ticket_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 0: return None
        return get_object_or_404(Ticket, pk=pk)

    def get_queryset(self):
        project = get_object_or_404(Project, key=self.kwargs.get('key'))
        return Ticket.objects.filter(project=project).order_by('-date_reported')

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, key=self.kwargs.get('key'))
        display_ticket = self.get_object()
        comments = Comment.objects.filter(ticket=display_ticket).order_by('-timestamp')
        comment_form = CommentForm()

        context = super().get_context_data(**kwargs)
        context['display_ticket'] = display_ticket
        context['project'] = project
        context['comments'] = comments
        context['comment_form'] = comment_form

        return context


class UserTicketListView(ListView):
    model = Ticket
    template_name = 'pybug/user_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ticket.objects.filter(reporter=user).order_by('-date_reported')


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['project', 'title', 'description', 'assignee']

    def get_initial(self):
        initial = super().get_initial()
        initial['project'] = self.request.GET.get('project')
        return initial

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['title', 'description', 'assignee', 'priority']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.reporter


def about(request):
    return render(request, template_name='pybug/about.html', context={'title': 'About'})
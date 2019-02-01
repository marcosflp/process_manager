from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from core.forms import ProfileForm, ProcessForm, ProcessFeedbackForm
from core.models import Profile, Process, ProcessFeedback


class BaseListView(ListView):
    paginate_by = 50


class BaseDetailView(DetailView):
    pass


class BaseCreateView(CreateView):
    pass


class BaseUpdateView(UpdateView):
    pass


class BaseDeleteView(DeleteView):
    pass


class HomeView(TemplateView):
    template_name = 'core/base.html'


class ProfileListView(BaseListView):
    model = Profile
    queryset = Profile.objects.all()


class ProfileCreateView(BaseCreateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile-list-view')

    @transaction.atomic
    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )
        user.set_password(form.cleaned_data['password'])
        user.save()

        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()

        return super(ProfileCreateView, self).form_valid(form)


class ProfileUpdateView(BaseUpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile-list-view')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user.username = form.cleaned_data['email']
        self.object.user.email = form.cleaned_data['email']
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        if form.cleaned_data['password']:
            self.object.user.set_password(form.cleaned_data['password'])
        self.object.user.save()
        return super(ProfileUpdateView, self).form_valid(form)


class ProfileDeleteView(BaseDeleteView):
    model = Profile
    success_url = reverse_lazy('profile-list-view')


class ProcessListView(BaseListView):
    model = Process
    queryset = Process.objects.all()


class ProcessCreateView(BaseCreateView):
    model = Process
    form_class = ProcessForm
    success_url = reverse_lazy('process-list-view')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super(ProcessCreateView, self).form_valid(form)


class ProcessUpdateView(BaseUpdateView):
    model = Process
    form_class = ProcessForm
    success_url = reverse_lazy('process-list-view')


class ProcessDetailView(BaseDetailView):
    model = Process


class ProcessDeleteView(BaseDeleteView):
    model = Process
    success_url = reverse_lazy('process-list-view')


class ProcessFeedbackCreateView(CreateView):
    model = ProcessFeedback
    form_class = ProcessFeedbackForm
    success_url = reverse_lazy('process-list-view')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.process = Process.objects.get(pk=self.kwargs['process_pk'])
        self.object.created_by = self.request.user
        self.object.save()
        return super(ProcessFeedbackCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ProcessFeedbackCreateView, self).get_context_data(**kwargs)
        data['process'] = Process.objects.get(pk=self.kwargs['process_pk'])
        return data


class ProcessFeedbackUpdateView(BaseUpdateView):
    model = ProcessFeedback
    form_class = ProcessFeedbackForm

    def get_success_url(self):
        return reverse('process-detail-view',
                       kwargs={'pk': self.kwargs['process_pk']})

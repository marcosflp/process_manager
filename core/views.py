from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView)
from rules.contrib.views import PermissionRequiredMixin

from core.forms import ProfileForm, ProcessForm, ProcessFeedbackForm
from core.models import Profile, Process, ProcessFeedback


class BaseListView(PermissionRequiredMixin, ListView):
    paginate_by = 50


class BaseDetailView(PermissionRequiredMixin, DetailView):
    pass


class BaseCreateView(PermissionRequiredMixin, CreateView):
    pass


class BaseUpdateView(PermissionRequiredMixin, UpdateView):
    pass


class BaseDeleteView(PermissionRequiredMixin, DeleteView):
    pass


class HomeView(TemplateView):
    template_name = 'core/base.html'


class ProfileListView(BaseListView):
    model = Profile
    queryset = Profile.objects.all()
    permission_required = 'admin_user'


class ProfileCreateView(BaseCreateView):
    model = Profile
    form_class = ProfileForm
    permission_required = 'admin_user'

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

        # The user Profile will be created at core.models.create_profile
        # with post_save signal.

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile-list-view')


class ProfileUpdateView(BaseUpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile-list-view')
    permission_required = 'admin_user'

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
    permission_required = 'admin_user'


class ProcessListView(BaseListView):
    model = Process
    permission_required = 'core.list_process'

    def get_queryset(self):
        queryset = super(ProcessListView, self).get_queryset()

        if self.request.user.has_perm('admin_user'):
            # show all
            pass
        elif self.request.user.has_perm('manager_user'):
            # show all
            pass
        elif self.request.user.has_perm('publisher_user'):
            # Show only Processes that the publisher are member
            queryset = queryset.filter(feedback_users=self.request.user)
        else:
            queryset = queryset.none()

        return queryset


class ProcessCreateView(BaseCreateView):
    model = Process
    form_class = ProcessForm
    success_url = reverse_lazy('process-list-view')
    permission_required = 'core.create_process'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super(ProcessCreateView, self).form_valid(form)


class ProcessUpdateView(BaseUpdateView):
    model = Process
    form_class = ProcessForm
    success_url = reverse_lazy('process-list-view')
    permission_required = 'core.update_process'


class ProcessDetailView(BaseDetailView):
    model = Process
    permission_required = 'core.view_process'


class ProcessDeleteView(BaseDeleteView):
    model = Process
    success_url = reverse_lazy('process-list-view')
    permission_required = 'core.delete_process'


class ProcessFeedbackCreateView(BaseCreateView):
    model = ProcessFeedback
    form_class = ProcessFeedbackForm
    success_url = reverse_lazy('process-list-view')
    permission_required = 'core.create_processfeedback'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.process = self.get_process()
        self.object.created_by = self.request.user
        self.object.save()
        return super(ProcessFeedbackCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ProcessFeedbackCreateView, self).get_context_data(**kwargs)
        data['process'] = Process.objects.get(pk=self.kwargs['process_pk'])
        return data

    def get_process(self):
        try:
            return Process.objects.get(pk=self.kwargs['process_pk'])
        except Process.DoesNotExist:
            raise Http404

    def get_permission_object(self):
        return self.get_process()


class ProcessFeedbackUpdateView(BaseUpdateView):
    model = ProcessFeedback
    form_class = ProcessFeedbackForm
    permission_required = 'core.update_processfeedback'

    def get_success_url(self):
        return reverse(
            'process-detail-view',
            kwargs={'pk': self.kwargs['process_pk']}
        )

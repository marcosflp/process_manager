from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from core.forms import ProfileForm
from core.models import Profile


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

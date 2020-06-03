from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DeleteView


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OwnerListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

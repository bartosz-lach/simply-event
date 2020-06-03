from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView

from simply_event_app.forms import UserRegisterForm, EventForm, GuestForm
from simply_event_app.models import Event, Guest
from simply_event_app.owner import OwnerCreateView, OwnerListView, OwnerUpdateView, OwnerDeleteView


def register_page(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            text_message = f'Hello {user.username}, your account was created'
            messages.success(request, text_message)
            return redirect('login.html')
    return render(request, 'auth/registration.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('simply_event_app:event_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('simply_event_app:event_list')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'auth/login.html')


def logout_user(request):
    logout(request)
    return redirect('simply_event_app:login_page')


class EventListView(ListView):
    model = Event
    paginate_by = 10
    template_name = 'simply_event_app/event_list.html'
    queryset = Event.objects.filter(is_public=True).order_by('start_date')


class UserEventListView(ListView):
    model = Event
    template_name = 'simply_event_app/event_list.html'

    def get_queryset(self):
        user_id = get_object_or_404(User, username=self.kwargs['slug']).id
        return super().get_queryset().filter(owner=user_id, is_public=True)


class OwnerEventListView(OwnerListView):
    model = Event
    template_name = 'simply_event_app/owner_event_list.html'


class EventCreateView(OwnerCreateView):
    form_class = EventForm
    template_name = 'simply_event_app/event_form.html'

    def get_success_url(self):
        return reverse('simply_event_app:event_detail', args=(self.object.id,))


class EventUpdateView(OwnerUpdateView):
    form_class = EventForm
    template_name = 'simply_event_app/event_form.html'
    queryset = Event.objects.all()

    def get_success_url(self):
        return reverse('simply_event_app:event_detail', args=(self.object.id,))


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        event = self.get_object()
        is_owner = event.owner.username == str(self.request.user)
        guests = event.guest_set.all()

        def add_time_with_delay(guest) -> dict:
            time_with_delay = guest.add_delay_to_date()
            guest = guest.to_dict()
            guest['time_with_delay'] = time_with_delay
            return guest

        guests = [add_time_with_delay(guest) for guest in guests]

        context = super().get_context_data()
        context['guests'] = guests
        context['is_owner'] = is_owner
        return context


class EventDeleteView(OwnerDeleteView):
    model = Event
    success_url = reverse_lazy('simply_event_app:owner_event_list')


class GuestDeleteView(DeleteView):
    model = Guest

    def get_queryset(self):
        return super().get_queryset().filter(event__owner=self.request.user)

    def get_success_url(self):
        guest = self.get_object()
        return reverse_lazy('simply_event_app:event_detail', args=(guest.event.id,))


class GuestCreateView(CreateView):
    form_class = GuestForm
    template_name = 'simply_event_app/guest_form.html'

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        print(event)
        return event

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        event = self.get_queryset()
        context['event_name'] = event.name
        return context

    def get_success_url(self):
        return reverse('simply_event_app:event_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        event = self.get_queryset()
        self.object = form.save(commit=False)
        self.object.event = event
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'You joined to the event')
        return super().form_valid(form)

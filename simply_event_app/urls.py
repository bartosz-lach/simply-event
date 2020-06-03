from django.urls import path, reverse
from . import views


app_name = 'simply_event_app'
urlpatterns = [
    path('accounts/registration/', views.register_page, name='registration_page'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/logout/', views.logout_user, name='logout_user'),

    path('', views.EventListView.as_view(), name='event_list'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('accounts/events/', views.OwnerEventListView.as_view(), name='owner_event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('guests/<int:pk>/', views.GuestDeleteView.as_view(), name='guest_delete'),
    path('events/<int:pk>/join/', views.GuestCreateView.as_view(), name='quest_create'),
    path('<slug:slug>/events/', views.UserEventListView.as_view(), name='user_event_list'),
]


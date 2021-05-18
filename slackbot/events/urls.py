from django.urls import path
from .views import SlackOffers, SlackCommands

urlpatterns = [
    path('offers/', SlackOffers.as_view(), name='event_hook'),
    path('commands/', SlackCommands.as_view(), name='slack_command')
]

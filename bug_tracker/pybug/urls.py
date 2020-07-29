from django.urls import path, include
from .views import (
    ProjectlistView,
    ProjectCreateView,
    TicketListView,
    TicketCreateView, 
    TicketUpdateView,
    TicketDeleteView,
    UserTicketListView,
    TicketAPIView,
    TicketDetailAPIView,
    ProjectAPIView,
    ProjectDetailAPIView,
)
from . import views


app_urlpatterns = [
    path('', ProjectlistView.as_view(), name='pybug-projects'),
    path('user/<str:username>/', UserTicketListView.as_view(), name='user-tickets'),
    path('project/<str:key>/tickets/<int:pk>/', TicketListView.as_view(), name='project-detail'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('ticket/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]


api_urlpatterns = [
    path('api/tickets/', TicketAPIView.as_view()),
    path('api/ticket/<int:pk>', TicketDetailAPIView.as_view()),
    path('api/projects/', ProjectAPIView.as_view()),
    path('api/project/<int:pk>', ProjectDetailAPIView.as_view()),
]


urlpatterns = [
    path('', include(app_urlpatterns)),
    path('', include(api_urlpatterns)),
]
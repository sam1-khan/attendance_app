from django.urls import path
from . import views

app_name='attendance'
urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='all'),
    path('attendance/<int:pk>/set_checkout/', views.SetCheckoutView.as_view(), name='set_check_out'),
    path('attendance/checkin/', views.SetCheckinView.as_view(), name='set_check_in'),
]
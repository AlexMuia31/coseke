from django.urls import path
from .views import MinuteList, MinutesDetail


urlpatterns = [
    path('minutes/', MinuteList.as_view(), name='minutes'),
    path('<pk>/', MinutesDetail.as_view(), name='details'),

]

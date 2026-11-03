from .views import IndexView, login_view, callback_view
from django.urls import path
urlpatterns = [
   path('', IndexView.as_view(), name='index'),
   path('login/', login_view, name='login'),
   path('complete/ion', callback_view, name='callback')
]

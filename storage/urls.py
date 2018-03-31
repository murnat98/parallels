from django.urls import path

from storage.views import KeyList

app_name = 'storage'

urlpatterns = [
    path('', KeyList.as_view()),
]

from django.urls import path

from storage.views import KeyList, Key

app_name = 'storage'

urlpatterns = [
    path('', KeyList.as_view()),
    path('<int:key>/', Key.as_view()),
]

from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.FileUploadView.as_view()),
    path("access/<int:file_id>/<str:access_code>/", views.FileAccessView.as_view()),
]

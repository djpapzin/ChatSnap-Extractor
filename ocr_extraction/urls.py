from django.urls import path
from .views import ExtractionViews

urlpatterns = {
    path("extract_message/", ExtractionViews.as_view())
}
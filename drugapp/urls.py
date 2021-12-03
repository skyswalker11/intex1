from django.urls import path
from .views import indexPageView, searchPageView, drugPageView, prescriberPageView, editprescriberPageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("search/", searchPageView, name="search"),
    path("drug/", drugPageView, name="drug"),
    path("prescriber/", prescriberPageView, name="prescriber"),
    path("edit/prescriber/", editprescriberPageView, name="editprescriber"),
]


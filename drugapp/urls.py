from django.urls import path
from .views import indexPageView, drugPageView, filterDrugPageView\
, prescriberPageView, editprescriberPageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("drug/", drugPageView, name="drug"),
    path("filter_drug/", filterDrugPageView, name="filter_drug"),
    path("prescriber/", prescriberPageView, name="prescriber"),
    path("edit/prescriber/<int:npi>", editprescriberPageView, name="edit_prescriber"),
]


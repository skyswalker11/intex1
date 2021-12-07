from django.urls import path
from .views import indexPageView, drugPageView,drugdetailsPageView\
, prescriberPageView, editprescriberPageView, prescriberdetailsPageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("drug/", drugPageView, name="drug"),
    path("drugdetails/<int:drug_id>", drugdetailsPageView, name="drug_details"),
    path("prescriber/", prescriberPageView, name="prescriber"),
    path("prescriberdetails/<int:npi>", prescriberdetailsPageView, name="prescriber_details"),
    path("edit/prescriber/<int:npi>", editprescriberPageView, name="edit_prescriber"),
]


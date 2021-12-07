from django.urls import path
from .views import indexPageView, drugPageView,drugdetailsPageView\
, prescriberPageView, editprescriberPageView, prescriberdetailsPageView, createprescriberPageView\
, analysis1PageView, analysis2PageView, deleteprescriberPageView, prescriptionsPageView,putprescriberPageView\
, recomPageView

urlpatterns = [
    path("analysis1/", analysis1PageView, name="analysis1"),
    path("analysis2/", analysis2PageView, name="analysis2"),
    path("", indexPageView, name="index"),
    path("drug/", drugPageView, name="drug"),
    path("drugdetails/<int:drug_id>", drugdetailsPageView, name="drug_details"),
    path("prescriber/", prescriberPageView, name="prescriber"),
    path("prescriberdetails/<int:npi>", prescriberdetailsPageView, name="prescriber_details"),
    path("create/prescriber/",createprescriberPageView, name="create_prescriber"),
    path("putprescriberP/", putprescriberPageView, name="put_prescriber"),
    path("delete/prescriber/",deleteprescriberPageView, name="delete_prescriber"),
    path("edit/prescriber/", editprescriberPageView, name="edit_prescriber"),
    path("prescriptions/", prescriptionsPageView, name="prescriptions"),
    path("recom/", recomPageView, name ="recom"),
]


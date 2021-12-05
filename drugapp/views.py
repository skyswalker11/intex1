from django.shortcuts import render
from .models import Drug, Prescriber, Triple

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')


def drugPageView(request) :
    drugs = Drug.objects.all()

    context = {
        "drugs": drugs,
    }
    return render(request, 'drugapp/drug.html', context)


def filterDrugPageView(request):

    if request.method == 'POST' :
        drugName = request.POST.get('search','off')
        isOpioid  = "is_opioid" in request.POST

        if isOpioid == True and drugName != "":
           drugs =  Drug.objects.filter(is_opioid=True,drug_name__contains=drugName)

        elif isOpioid == True and drugName == "":
            drugs = Drug.objects.filter(is_opioid=True)
        elif isOpioid == False and drugName != "":
            drugs = Drug.objects.filter(drug_name__contains=drugName)
        else:
            return drugPageView(request)

        context = {
            "drugs": drugs,
        }

        return render(request, 'drugapp/drug.html', context)

    else:
        return drugPageView(request)


def prescriberPageView(request) :
    prescribers = Prescriber.objects.all()

    context = {
        "prescribers": prescribers,
    }
    return render(request, 'drugapp/prescriber.html', context)


def editprescriberPageView(request,npi) :

    prescriber = Prescriber.objects.get(npi=npi)
    triples = prescriber.triple_set.all()

    context = {
        "prescriber": prescriber,
        "triples": triples,
    }

    return render(request, 'drugapp/editprescriber.html', context)

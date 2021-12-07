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

def drugdetailsPageView(request,drug_id) :
    drug = Drug.objects.get(id=drug_id)
    triples = Triple.objects.filter(drug_id=drug_id).order_by('-quantity')[:10]

    context = {
        "drug": drug,
        "triples":triples
    }
    return render(request, 'drugapp/drugdetails.html', context)


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

def prescriberdetailsPageView(request,npi) :
    prescriber = Prescriber.objects.get(npi=npi)
    triples = Triple.objects.filter(npi=npi).order_by('-quantity')[:10]

    context = {
        "prescriber": prescriber,
        "triples":triples
    }
    return render(request, 'drugapp/prescriberdetails.html',context)
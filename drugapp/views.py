from django.shortcuts import render
from .models import Drug, Prescriber, Triple

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')


def drugPageView(request) :

    #Search Functionality
    if request.method == 'POST' :
        drugName = request.POST.get('search','off').upper()
        filter = request.POST.get('filter')

        if drugName != "":
            if filter == 'opioid':
                drugs = Drug.objects.filter(drug_name__contains=drugName,is_opioid=True)
            elif filter == 'non_opioid':
                drugs = Drug.objects.filter(drug_name__contains=drugName,is_opioid=False)
            else:   
                drugs =  Drug.objects.filter(drug_name__contains=drugName)
        else :
            if filter == 'opioid':
                drugs = Drug.objects.filter(is_opioid=True)
            elif filter == 'non_opioid':
                drugs = Drug.objects.filter(is_opioid=False)
            else:   
                drugs =  Drug.objects.all()

        context = {
            "drugs": drugs,
        }

        return render(request, 'drugapp/drug.html', context)

    #Default view
    else:
        drugs = Drug.objects.all()

        context = {
            "drugs": drugs,
        }
        return render(request, 'drugapp/drug.html', context)


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
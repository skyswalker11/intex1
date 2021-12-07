from django.shortcuts import render
from django.db.models import Q
from .models import Drug, Prescriber, Triple, State

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')


def drugPageView(request) :

    #Search Functionality
    if request.method == 'POST' :
        search = request.POST.get('search')
        filter = request.POST.get('filter')

        if search != "":
            if filter == 'opioid':
                drugs = Drug.objects.filter(drug_name__contains=search,is_opioid=True)
            elif filter == 'non_opioid':
                drugs = Drug.objects.filter(drug_name__contains=search,is_opioid=False)
            else:   
                drugs =  Drug.objects.filter(drug_name__contains=search)
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


def drugdetailsPageView(request,drug_id):
    drug = Drug.objects.get(id=drug_id)
    triples = Triple.objects.filter(drug_id=drug_id).order_by('-quantity')[:10]

    context = {
        "drug": drug,
        "triples":triples
    }
    return render(request, 'drugapp/drugdetails.html', context)


def prescriberPageView(request) :

    #Search Functionality
    if request.method == 'POST' :
        search = request.POST.get('search')
        state = request.POST.get('state')
        filter = request.POST.get('filter')

        #Dumb filter, cant fiture out how to shrink this...
        if state != 'all':
            if search != "":
                if filter == 'male':
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search), gender='M',state__state=state)[:1000]

                elif filter == 'female':
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search), gender='F',state__state=state)[:1000]
                else:   
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search),state__state=state)[:1000]
            else :
                if filter == 'male':
                    prescribers = Prescriber.objects.filter(gender='M',state__state=state)[:1000]
                elif filter == 'female':
                    prescribers = Prescriber.objects.filter(gender='F',state__state=state)[:1000]
                else:   
                    prescribers =  Prescriber.objects.filter(state__state=state)[:1000]

        else:
            if search != "":
                if filter == 'male':
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search), gender='M')[:1000]

                elif filter == 'female':
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search), gender='F')[:1000]
                else:   
                    prescribers = Prescriber.objects.filter(Q(first_name__icontains=search) \
                        | Q(last_name__icontains=search) | Q(credentials__icontains=search) \
                        | Q(specialty__icontains=search))[:1000]
            else :
                if filter == 'male':
                    prescribers = Prescriber.objects.filter(gender='M')[:1000]
                elif filter == 'female':
                    prescribers = Prescriber.objects.filter(gender='F')[:1000]
                else:   
                    prescribers =  Prescriber.objects.all()[:1000]

                    
            
        states = State.objects.all()

        context = {
            "prescribers": prescribers,
            "states": states,
        }

        return render(request, 'drugapp/prescriber.html', context)

    #Default view
    else:
        prescribers = Prescriber.objects.all()[:1000]
        states = State.objects.all()

        context = {
            "prescribers": prescribers,
            "states": states,
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
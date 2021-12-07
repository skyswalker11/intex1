from django.shortcuts import render
from django.db.models import Q, Sum
from .models import Drug, Prescriber, Triple, State
import psycopg2

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')

# Queries Database
def analysis1PageView(request) :
    
    con = psycopg2.connect(database='intex_operational', user='postgres',
        password='admin')

    with con:
        cur = con.cursor()

        cur.execute("""select p.First_name, p.Last_name,sum(quantity) Opioid_Prescriptions, t.npi from pd_prescriber p
                        join pd_prescriber_drug_triple t on p.npi = t.npi
                        join pd_drug d on t.drug_id = d.id
                        where d.is_opioid = true
                        group by t.npi, p.first_name, p.last_name
                        order by Opioid_Prescriptions desc
                        """)
        
        results = cur.fetchall()
                    

        cur = con.cursor()

        cur.execute("""select drug_name, sum(quantity) Total_Prescriptions from pd_prescriber p
                        join pd_prescriber_drug_triple t on p.npi = t.npi
                        join pd_drug d on t.drug_id = d.id
                        group by drug_name
                        order by Total_Prescriptions desc;

                        """)
        
        results2 = cur.fetchall()
    
        cur = con.cursor()

        cur.execute("""select drug_name, sum(quantity) Total_Prescriptions from pd_prescriber p
                        join pd_prescriber_drug_triple t on p.npi = t.npi
                        join pd_drug d on t.drug_id = d.id
                        where d.is_opioid = true
                        group by drug_name
                        order by Total_Prescriptions desc;

                        """)
        
        results3 = cur.fetchall()
   
    context = {
            "results" : results,
            "results2" : results2,
            "results3" : results3
        } 
    return render(request, 'drugapp/analysis1.html', context)

# Queries Database
def analysis2PageView(request) :
    
    con = psycopg2.connect(database='intex_operational', user='postgres',
        password='admin')

    with con:
        cur = con.cursor()

        cur.execute("""select state, death_count from pd_state_data
                        group by state, death_count
                        order by death_count desc;
                        """)
        
        resultsB = cur.fetchall()
                    

        cur = con.cursor()

        cur.execute("""select s.state, d.drug_name, sum(quantity) Total_Prescriptions from pd_drug d
                        join pd_prescriber_drug_triple t
                            on d.id = t.drug_id
                        join pd_prescriber p 
                            on t.npi = p.npi
                        join pd_state_data s 
                            on p.state = s.state_abbrev
                    where is_opioid = true
                    group by d.id, t.drug_id, s.state;
                    """)
        
        results2B = cur.fetchall()
    
        cur = con.cursor()

        cur.execute("""select drug_name, sum(quantity) Total_Prescriptions from pd_prescriber p
                        join pd_prescriber_drug_triple t on p.npi = t.npi
                        join pd_drug d on t.drug_id = d.id
                        where d.is_opioid = true
                        group by drug_name
                        order by Total_Prescriptions desc;

                        """)
        
        results3B = cur.fetchall()
  
    context = {
            "resultsB" : resultsB,
            "results2B" : results2B,
            "results3B" : results3B
        } 
    return render(request, 'drugapp/analysis2.html', context)

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
    sum = Triple.objects.filter(drug_id=drug_id).aggregate(Sum('quantity'))

    context = {
        "drug": drug,
        "triples":triples,
        "sum": sum
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


def prescriberdetailsPageView(request,npi) :
    prescriber = Prescriber.objects.get(npi=npi)
    triples = Triple.objects.filter(npi=npi).order_by('-quantity')[:10]

    context = {
        "prescriber": prescriber,
        "triples":triples
    }

    return render(request, 'drugapp/prescriberdetails.html',context)


def createprescriberPageView(request) :

    if request.method == 'POST' : 
<<<<<<< HEAD
        npi = request.POST['npi']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        state = request.POST['state']
        thisState = State.objects.get(state_abbrev=state)
        credendtials = request.POST['credendtials']
        specialty = request.POST['specialty']
        opiate = request.POST['opiate']
        prescriptions = request.POST['prescriptions']

        if opiate == 'y':
            opiate = True
        else :
            opiate = False

        instance = Prescriber(npi=npi,first_name=fname,last_name=lname,gender=gender,\
            state=thisState,credentials=credendtials,specialty=specialty,is_opioid_prescriber=opiate,total_prescriptions=prescriptions)

        instance.save()

        return prescriberdetailsPageView(request,npi)
=======
        #create new prescriber
        new_prescriber = Prescriber('123','joe','smith','m','UT','MD','Family','T','1234')
        #store data from form to new object
        new_prescriber.npi = request.POST.get('npi')
                
        new_prescriber.first_name = request.POST.get('fname')

        new_prescriber.last_name = request.POST.get('lname')

        new_prescriber.gender = request.POST.get('gender')

        new_prescriber.state = request.POST.get('state_abbrev')

        new_prescriber.credentials = request.POST.get('credentials')

        new_prescriber.specialty = request.POST.get('specialty')

        new_prescriber.is_opioid_prescriber = request.POST.get('opiate')

        new_prescriber.total_prescriptions = request.POST.get('prescriptions')
        
        new_state = State.objects.get(state_abbrev = request.POST.get('state'))
    
        new_prescriber.state = new_state

        new_prescriber.save()

        data = new_prescriber.npi

        states = State.objects.all()
        context = {
            "prescribers" : data,
        }
        return prescriberdetailsPageView(request, data)
>>>>>>> bf188e7e25384fde00811b076ae3c5e9364deb08
    
    else:
        states = State.objects.all()

        context = {
            "states": states,
        }

        return render(request, 'drugapp/createPrescriber.html', context)


def editprescriberPageView(request) :

    if request.method == 'POST' : 
        npi = request.POST['npi']
        prescriber = Prescriber.objects.get(npi=npi)
        states = State.objects.all()

        context = {
            "prescriber": prescriber,
            "states": states,
        }

        return render(request, 'drugapp/editprescriber.html', context)

    else:
        prescribers = Prescriber.objects.all()[:1000]
        states = State.objects.all()

        context = {
            "prescribers": prescribers,
            "states": states,
        }

        return render(request, 'drugapp/prescriber.html', context)

def putprescriberPageView(request):
    if request.method == 'POST' : 
        npi = request.POST['npi']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        state = request.POST['state']
        thisState = State.objects.get(state_abbrev=state)
        credendtials = request.POST['credendtials']
        specialty = request.POST['specialty']
        opiate = request.POST['opiate']
        prescriptions = request.POST['prescriptions']

        if opiate == 'y':
            opiate = True
        else :
            opiate = False

        instance = Prescriber(npi=npi,first_name=fname,last_name=lname,gender=gender,\
            state=thisState,credentials=credendtials,specialty=specialty,is_opioid_prescriber=opiate,total_prescriptions=prescriptions)

        instance.save()

        return prescriberdetailsPageView(request,npi)
    
    else:
        states = State.objects.all()

        context = {
            "states": states,
        }

        return render(request, 'drugapp/prescriber.html', context)



def deleteprescriberPageView(request):

    if request.method == 'POST' : 
        npi = request.POST['npi']
        instance = Prescriber.objects.get(npi=npi)
        instance.delete()

    prescribers =  Prescriber.objects.all()[:1000]
    states = State.objects.all()

    context = {
        "prescribers": prescribers,
        "states": states,
    }

    return render(request, 'drugapp/prescriber.html', context)


def prescriptionsPageView(request):
    return render(request, 'drugapp/prescriptions.html')
from django.shortcuts import render
from .models import Drug, Prescriber, Triple
import psycopg2

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')

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
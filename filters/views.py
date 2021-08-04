import json

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django_xhtml2pdf.utils import generate_pdf

# Create your views here.
temp = {}
college_df = pd.read_csv('./college_main.csv')
q = {0: 'General', 1: 'OBC-A', 2: 'OBC-B', 3: 'Scheduled-Caste', 4: 'Scheduled-Tribe'}
k = 0
department = {100: 'All', 0: 'Computer Science', 1: 'Information Technology', 2: 'Electrical Engineering',
              3: 'Electronics and Communication Engineering', 4: 'Mechanical Engineering'}
affiliation = {0: 'All', 1: 'G', 2: 'P'}
uniquelocation = college_df['LOCATION'].unique()

location = {i: uniquelocation[i] for i in range(0, len(uniquelocation))}
location[100] = 'Any'
query = 0


def index(request):
    global temp
    temp['rank'] = 1
    temp['quota'] = 0
    temp['dept'] = 0
    temp['affil'] = 0
    temp['location'] = 100
    context = {'temp': temp}
    return render(request, 'home.html', context)


def predict_rank(request):
    global temp
    if request.method == 'POST':
        temp['rank'] = int(request.POST.get('rank'))
        gmr = 1
    context = {'temp': temp, 'gmr': gmr}
    return render(request, 'home.html', context)


def find_college(request):
    # college_df = pd.read_csv('./college_main.csv')
    global college_df
    college_df = pd.read_csv('./college_main.csv')
    global temp
    global q
    global k
    if request.method == 'POST':
        temp['quota'] = int(request.POST.get('quota'))

        k = temp['quota']
        if k == 0:
            college_df = college_df.loc[
                (college_df[['CSE GMR', 'IT GMR', 'EE GMR', 'ME GMR', 'ECE GMR']].max(axis=1)) >= temp['rank']]
            college_df.rename({'CSE GMR': 'CSE', 'IT GMR': 'IT', 'EE GMR': 'EE', 'ME GMR': 'ME', 'ECE GMR': 'ECE'},
                              axis=1, inplace=True)
        elif k == 1:
            college_df = college_df.loc[
                (college_df[['CSE OBCA', 'IT OBCA', 'EE OBCA', 'ME OBCA', 'ECE OBCA']].max(axis=1)) >= temp['rank']]
            college_df.rename({'CSE OBCA': 'CSE', 'IT OBCA': 'IT', 'EE OBCA': 'EE', 'ME OBCA': 'ME', 'ECE OBCA': 'ECE'},
                              axis=1, inplace=True)
        elif k == 2:
            college_df = college_df.loc[
                (college_df[['CSE OBCB', 'IT GMR', 'EE OBCB', 'ME OBCB', 'ECE OBCB']].max(axis=1)) >= temp['rank']]
            college_df.rename({'CSE OBCB': 'CSE', 'IT OBCB': 'IT', 'EE OBCB': 'EE', 'ME OBCB': 'ME', 'ECE OBCB': 'ECE'},
                              axis=1, inplace=True)
        elif k == 3:
            college_df = college_df.loc[
                (college_df[['CSE SC', 'IT SC', 'EE SC', 'ME SC', 'ECE SC']].max(axis=1)) >= temp['rank']]
            college_df.rename({'CSE SC': 'CSE', 'IT SC': 'IT', 'EE SC': 'EE', 'ME SC': 'ME', 'ECE SC': 'ECE'}, axis=1,
                              inplace=True)
        elif k == 4:
            college_df = college_df.loc[
                (college_df[['CSE ST', 'IT ST', 'EE ST', 'ME ST', 'ECE ST']].max(axis=1)) >= temp['rank']]
            college_df.rename({'CSE ST': 'CSE', 'IT ST': 'IT', 'EE ST': 'EE', 'ME ST': 'ME', 'ECE ST': 'ECE'}, axis=1,
                              inplace=True)

        json_records = college_df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        gmr = 1

        context = {'temp': temp, 'gmr': gmr, 'd': data, 'q': q.get((k))}
        return render(request, 'showtable.html', context)


def departmentwise(request):
    global college_df
    global temp
    global q
    global k
    if request.method == 'POST':
        temp['dept'] = int(request.POST.get('dept'))
        temp['affil'] = int(request.POST.get('affil'))
        temp['location'] = int(request.POST.get('location'))

    dep = temp['dept']
    af = temp['affil']
    lo = temp['location']

    if dep == 0:
        college_dfc = college_df.loc[
            (college_df['CSE'] >= temp['rank']) & (
                    (college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                    (college_df['LOCATION'] == location.get((lo))) | (temp['location'] == 100))]
        json_records = college_dfc.reset_index().to_json(orient='records')
    if dep == 1:
        college_dfi = college_df.loc[(college_df['IT'] >= temp['rank']) & (
                (college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                                             (college_df['LOCATION'] == location.get((lo))) | (
                                             temp['location'] == 100))]
        json_records = college_dfi.reset_index().to_json(orient='records')
    if dep == 2:
        college_dfee = college_df.loc[(college_df['EE'] >= temp['rank']) & (
                (college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                                              (college_df['LOCATION'] == location.get((lo))) | (
                                              temp['location'] == 100))]
        json_records = college_dfee.reset_index().to_json(orient='records')
    if dep == 4:
        college_dfm = college_df.loc[(college_df['ME'] >= temp['rank']) & (
                (college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                                             (college_df['LOCATION'] == location.get((lo))) | (
                                             temp['location'] == 100))]
        json_records = college_dfm.reset_index().to_json(orient='records')
    if dep == 3:
        college_dfece = college_df.loc[
            (college_df['ECE'] >= temp['rank']) & (
                    (college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                    (college_df['LOCATION'] == location.get((lo))) | (temp['location'] == 100))]
        json_records = college_dfece.reset_index().to_json(orient='records')
    if dep == 100:
        college_dfg = college_df.loc[((college_df['GOVERNMENT'] == affiliation.get((af))) | (temp['affil'] == 0)) & (
                (college_df['LOCATION'] == location.get((lo))) | (temp['location'] == 100))]
        json_records = college_dfg.reset_index().to_json(orient='records')

    data = []
    data = json.loads(json_records)

    context = {'temp': temp, 'd': data, 'q': q.get(k), 'dept': department.get(dep), 'dep': dep,
               'aff': affiliation.get(af), 'af': af, 'loc': location.get(lo), 'l': lo}
    return render(request, 'showtable.html', context)


def loan(request):
    global query
    query = request.GET.get('data')
    if query:
        query = int(query) * 8
    else:
        query = 0
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="loan-application.pdf"'
    context = {'query': query}
    result = generate_pdf('loan.html', file_object=resp, context=context)
    return result

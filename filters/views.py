from django.shortcuts import render
import pandas as pd
import json

# Create your views here.
temp={}

def index(request):
    temp['rank']=1
    temp['quota']=0
    temp['dept']=0
    temp['CSE GMR']= 1
    temp['IT GMR']= 1
    temp['ME GMR']=1
    temp['EE GMR']=1
    temp['ECE GMR']=1
    context={'temp':temp, 'cse_g':temp['CSE GMR'], 'it_g':temp['IT GMR'], 'me_g':temp['ME GMR'], 'ee_g':temp['EE GMR'], 'ece_g':temp['ECE GMR'] }
    return render(request,'home.html', context)

def predict_rank(request):
    college_df=pd.read_csv('./college_main.csv')

    if request.method=='POST':
        temp['rank']=int(request.POST.get('rank'))
        college_df=college_df.loc[college_df['ECE ST'] >= temp['rank']]
        # result= college_df.to_html(classes='table table-striped')
        # text_file = open("./templates/cutoff.html", "w")
        # text_file.write(result)
        # text_file.close()
        # json_records = college_df.reset_index().to_json(orient ='records')
        # data = []
        # data = json.loads(json_records)
        gmr=1
    context={'temp':temp,'gmr':gmr}
    return render(request, 'home.html', context)

def find_college(request):
    college_df=pd.read_csv('./college_main.csv')

    if request.method=='POST':
        temp['rank']=int(request.POST.get('rank'))
        temp['quota']=int(request.POST.get('quota'))

        k = temp['quota']
        if k==0:
            college_df=college_df.loc[college_df['CSE GMR'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT GMR'] >= temp['rank']]
            college_df=college_df.loc[college_df['EE GMR'] >= temp['rank']]
            college_df=college_df.loc[college_df['ME GMR'] >= temp['rank']]
            college_df=college_df.loc[college_df['ECE GMR'] >= temp['rank']]

        elif k==1:
            college_df=college_df.loc[college_df['CSE OBCA'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT OBCA'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE OBCA'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT OBCA'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE OBCA'] >= temp['rank']]

        elif k==2:
            college_df=college_df.loc[college_df['CSE OBCB'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT OBCB'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE OBCB'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT OBCB'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE OBCB'] >= temp['rank']]

        elif k==3:
            college_df=college_df.loc[college_df['CSE SC'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT SC'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE SC'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT SC'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE SC'] >= temp['rank']]

        elif k==4:
            college_df=college_df.loc[college_df['CSE ST'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT ST'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE ST'] >= temp['rank']]
            college_df=college_df.loc[college_df['IT ST'] >= temp['rank']]
            college_df=college_df.loc[college_df['CSE ST'] >= temp['rank']]

        json_records = college_df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        gmr=1
        q=1
        context={'temp':temp,'gmr':gmr, 'd':data, 'q':q, 'quota':temp['quota']}
        return render(request, 'showtable.html', context)




def departmentwise(request):
    college_df = pd.read_csv('./college_main.csv')
    if request.method=='POST':
        temp['rank']=int(request.POST.get('rank'))
        temp['dept']=int(request.POST.get('dept'))

    d = temp['dept']

    if d==0:
        college_df = college_df.loc[college_df['CSE GMR'] >= temp['rank']]

    if d==3:
        college_df = college_df.loc[college_df['ECE GMR'] >= temp['rank']]


    json_records = college_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    gmr = 1
    q = 1
    context = {'temp': temp, 'gmr': gmr, 'd': data, 'q': q, 'quota': temp['quota'], 'dept' : temp['dept']}
    return render(request, 'showtable.html', context)














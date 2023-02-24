from django.shortcuts import render
from django.http import HttpResponse
import json
Quetions=[]
area=""
dept = ""
doc = ""
slot = ""
indu=0
def ProcessData(data):
    global Quetions,dept,doc,slot,area,indu
    try:
        Quetion=Quetions[indu]
        print(Quetion,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>",data,"<<<<",indu)

        if data in ['thanks','thnx','thank you','ty','thanks alot','thank u', 'thank you very much']:
            return "You are welcome"
        if 'name' in Quetion:
            indu+=1
        elif 'age' in Quetion:

            indu+=1
        elif 'area' in Quetion:
            if int(data) <0 or int(data) >150:
                raise ValueError
            print("Area Quetion having area:" + area + ", dept:" + dept + ", doc:" + doc + ", slot:" + slot)
            Quetion+=", ".join(list(Jdata['Areas'].keys()))
            indu+=1
        elif 'department' in Quetion:
            area = data.lower()
            print("dept Quetion having area:" + area + ", dept:" + dept + ", doc:" + doc + ", slot:" + slot)
            Quetion += " , ".join(list(Jdata['Areas'][area].keys()))
            indu += 1
        elif 'Doctor' in Quetion:
            dept = data.lower()
            print("doc Quetion having area:" + area + ", dept:" + dept + ", doc:" + doc + ", slot:" + slot)
            Quetion += " ".join(list(Jdata['Areas'][area][dept].keys()))
            indu += 1
        elif 'slot' in Quetion:
            doc = data.title()
            print("slot Quetion having area:" + area + ", dept:" + dept + ", doc:" + doc + ", slot:" + slot)
            Quetion += " ".join(list(Jdata['Areas'][area][dept][doc]['Availbale slots']))
            indu+=1
        if data not in Receipt:
            Receipt.append(data.title())
        return Quetion
    except ValueError:
        Receipt.pop()
        return "Please enter valid age"
    except KeyError:
        print('''
        ****************
        *********
        ****************
        ''')
        Receipt.pop()
        return "Please enter valid choice"
    except IndexError:
        Jdata['Areas'][area][dept][doc]['Availbale slots'].remove(data.lower())
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>     "+ str(Jdata['Areas'][area][dept][doc]['Availbale slots']))
        with open(r'D:\Projects\MCA SEM 1 Mini-Project\Project Files\medbot_v1\ScheduleingData.json', 'w') as f:
            json.dump(Jdata, f)

        Receipt1=Receipt
        indu=0
        dept = ""
        doc = ""
        slot = ""

        return "Thank you "+str(Receipt1[1])+"("+str(Receipt1[2])+"). Your appointment to the ESI hospital's "+str(Receipt1[3])+"  branch with "+str(Receipt1[5])+" of "+str(Receipt1[4])+" department is scheduled on "+str(Receipt1[6])+" today."
# Create your views here.
Jdata=dict()
def show ( request) :
    global Quetions, Jdata, Receipt, indu
    indu=0
    with open(r'D:\Projects\MCA SEM 1 Mini-Project\Project Files\medbot_v1\ScheduleingData.json', 'r') as jsonfile:
        Jdata = json.load(jsonfile)
        Quetions = Jdata['Qset']
        Receipt=[]
    return render(request, "chatapp/index2.html")

Receipt=[]
def add(request):
    global Receipt
    if request.method == "GET":
        data= request.GET['que']
        Receipt.append(data)
        return HttpResponse(ProcessData(data))#
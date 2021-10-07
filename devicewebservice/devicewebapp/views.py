from django.shortcuts import render
import pymongo

from datetime import datetime as dt

#for post request with query
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request,'devicewebapp/index.html')

def viewdevices(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["UIOT"]
    mycol = mydb["Devices"]
    devconncol = mydb["DeviceConns"]

    viewdevices = []
    viewdeviceconns = []

    for device in mycol.find():
        viewdevices.append(device)

    for devconns in devconncol.find():
        viewdeviceconns.append(devconns)
        print(devconns)

    devdata = {'viewdevicesdata': viewdevices, 'viewdeviceconndata':viewdeviceconns}
    return render(request,'devicewebapp/viewdevices_lab3_part3.html',context=devdata)
    #return render(request,'devicewebapp/viewdevices_part3.html',context=devdata)
    #return render(request,'devicewebapp/viewdevices.html',context=devdata)

def devices(request,param1):
    dev_name = param1
    dtnow = dt.now()

    iotdev = { "name": dev_name, "datetime": dtnow }

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["UIOT"]
    mycol = mydb["Devices"]
    devconncol = mydb["DeviceConns"]

    viewdevices = []
    for device in mycol.find({'name':dev_name}):
        viewdevices.append(device)

    if (len(viewdevices) >= 1):
        iotdevlog={ "name": dev_name, "datetime": dtnow, "status":"updated" }
        y = devconncol.insert_one(iotdevlog)
        dev_name = "{} updated in DB".format(dev_name)
    else:
        x = mycol.insert_one(iotdev)
        iotdevlog={ "name": dev_name, "datetime": dtnow, "status":"new" }
        y = devconncol.insert_one(iotdevlog)
        dev_name = "{} device has been recorded!!".format(dev_name)

    return render(request, 'devicewebapp/devices.html', context={'data': dev_name})
    #return render(request, 'devicewebapp/devices.html', context={'data': iotdev, 'datalog': iotdevlog, 'msg_display': res_dev_name})

@csrf_exempt
def postview(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        passwd = request.POST.get('password')
        print("username:{} and password:{}".format(usrname,passwd))

        return HttpResponse("POST Request {} exist with {} - successful".format(usrname,passwd))
    elif request.method == 'GET':
        if request.GET.get('q','nothing'):
            qstring=request.GET.get('q',nothing)
            print("query string:{}".format(qstring))
            return HttpResponse("Query Done")
        else:
            usrname = request.GET.get('username')
            passwd = request.GET.get('password')
            print("username:{} and password:{} - GET successful".format(usrname,passwd))
            return HttpResponse("GET Request {} exist with {} - successful".format(usrname,passwd))

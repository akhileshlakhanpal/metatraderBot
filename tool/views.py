from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.shortcuts import render

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Please check your Password")
            return render(request, 'pages/login.html')
    else:
        return render(request, 'pages/login.html')

def dashboard(request):
    return render(request,'pages/dashboard.html')

def manage_slave(request):
    data_pass= {'masters': master_details.objects.values(), 'data': copier_details.objects.values()}
    if request.method == 'POST':
        master_account = request.POST['master_account']
        mt5_id = request.POST['mt5_id']
        password = request.POST['password']
        commission = request.POST['commission']
        risk = request.POST['risk']
        try:
            stop_loss = request.POST['stop_loss']
        except:
            stop_loss=''
        try:
            take_profit = request.POST['take_profit']
        except:
            take_profit=''
        try:
            reverse_trade = request.POST['reverse_trade']
        except:
            reverse_trade=''
        print(reverse_trade)
        status = request.POST['status']
        name = request.POST['name']

        en=copier_details(server_id=1,master_id=master_account,mt5_id=mt5_id,password=password,name=name,
                          commission=commission,risk=risk,stop_loss=True if stop_loss == 'on' else False,
                          take_profit=True if take_profit == 'on' else False,reverse_trade=True if reverse_trade == 'on' else False,status= True if status == 'on' else False)
        en.save()
        return redirect('/manage_slave')
    return render(request,'pages/manage_slave.html',data_pass)

def manage_master(request):
    data_pass={'data':master_details.objects.select_related('server_id').values('server_id__server_name','server_id__company_name','mt5_id','id','status','name')}
    if request.method == 'POST':
        mt5_id = request.POST['mt5_id']
        password = request.POST['password']
        commission = request.POST['commission']
        description = request.POST['description']
        status = request.POST['status']
        identical = request.POST['identical']
        name = request.POST['name']

        en = master_details(server_id=1, mt5_id=mt5_id, password=password, name=name,
                            commission=commission,description=description, status=True if status == 'on' else False,set_identical=True if identical == 'on' else False)
        en.save()
        return redirect('/manage_master')
    return render(request,'pages/manage_master.html',data_pass)

def groups_copier(request):
    return render(request,'pages/groups_copier.html')

def servers(request):
    data_pass={'data':server_details.objects.values()}
    if request.method == 'POST':
        company_name = request.POST['company_name']
        server_name = request.POST['server_name']
        server_ip = request.POST['server_ip']
        server_id = request.POST['server_id']
        api_url = request.POST['api_url']
        password = request.POST['password']
        status = request.POST['status']

        en = server_details(company_name=company_name, server_name=server_name, server_password=password, api_url=api_url,
                            serer_ip=server_ip,server_id=server_id, status=status)
        en.save()
        return redirect ('/servers')
    return render(request,'pages/servers.html',data_pass)
from django.shortcuts import render,redirect
import shutil
from nessus import nessus,get_config
from django.shortcuts import HttpResponse
import os
import ToMulVAL.editable_table.utils.DBO as DB
import ToMulVAL.editable_table.utils.ToMulval as TM
from django.http import JsonResponse
import json

def toMulVAL(req):
    return render(req, "toMulVAL.html")

def tomulvalupload(req):
    # shutil.rmtree('./ToMulVAL/upload')
    # os.mkdir('./ToMulVAL/upload')
    # print("data: ", req.POST)
    # print("file:", req.FILES)
    if req.method == "POST":
        file = req.FILES.get("upload", None)
        if not file:
            return render(req, "ToMulVAL.html", {"errinf":"No files for upload!"})
        # f = open("./ToMulVAL/upload/test.nessus", 'wb')
        # print("sadasd",file)
        # f = open("./ToMulVAL/upload/"+file.name, 'wb+')
        f = open(os.path.join("./ToMulVAL/upload",file.name), 'wb+')
        for line in file.chunks():  # 分块写入
            f.write(line)
        f.close()
    path = os.path.join("./ToMulVAL/upload",file.name)
    nessus(path)
    # return render(req,"toMulVAL.html")
    return redirect('/ToMulVAL/tomulvalerror1/')


def tomulvalerror1(req):
    return render(req, "toMulVAL.html", {"errinf": "successful file! "})


def tomulvaldownload(request):
    file=open('./ToMulVAL/download/nessus.P','rb')
    response=HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="nessus.P"'
    return response

def tomulvaldownload1(request):
    file=open('./input.P','rb')
    response=HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="AG_input.P"'
    return response


def GetData(request):
    global tpname
    if request.is_ajax():
        dic = request.POST
    tpname = dic["topo"]
    dbo = DB.DBO(tpname)
    dic = dbo.RetTabEle()
    dbo.close()
    response = JsonResponse(dic)
    return response

def PostData(request):
    global tpname
    dbo = DB.DBO(tpname)
    if request.is_ajax():
        dic = request.POST
    v1 = dic["table"]
    v2 = json.loads(v1)
    dbo.Infoupdate(v2)
    dbo.CVEupdate(v2)

    dbo.close()
    response = JsonResponse({"hello": "hi"})
    return response

def GenMulval(request):
    print(tpname)
    tom = TM.ToM(tpname)
    print('p1')
    tom.GenM(tom.Gettup())
    print('p2')
    response = JsonResponse({"hello": "hi"})
    return response


def setlist(req):
    return render(req, "list.html")

def GetList(request):
    global tpname
    list = []
    if request.is_ajax():
        dic = request.POST
        tpname = dic["topo"]
        # print(tpname)
        dbo = DB.DBO(tpname)
        dic = dbo.GetAllByCidr()
        num = 1
        for i1 in dic.keys():
            subnum = 1
            list.append({'id': str(num), 'ip': i1+'（主机数：'+str(len(dic[i1]))+'）'})
            for i2 in dic[i1]:
                list.append({'pid': str(num),'id': str(num)+'_'+str(subnum), 'ip': i2[1], 'name': i2[12], 'mac': i2[0], 'mod': i2[2], 'cve': i2[4], 'manu': i2[8], 'attr': '外网接入：'+i2[10]+' ; '+'读写服务：'+i2[11], 'wr': i2[14], 'rr': i2[15]})
                subnum += 1
            num += 1
    re = {'list':json.dumps(list)}
    response = JsonResponse(re)
    return response
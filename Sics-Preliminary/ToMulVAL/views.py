from django.shortcuts import render,redirect
import shutil
from nessus import nessus,get_config
from django.shortcuts import HttpResponse
import os
import ToMulVAL.editable_table.utils.DBO as DB
import ToMulVAL.editable_table.utils.ToMulval as TM
from django.http import JsonResponse

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
    print(tpname)
    dbo = DB.DBO(tpname)
    dic = dbo.RetTabEle()
    response = JsonResponse(dic)
    return response

def PostData(request):
    dbo = DB.DBO(tpname)
    if request.is_ajax():
        dic = request.POST
    v1 = dic["table"]
    # print(v1)
    v2 = v1.split("\n")
    for i in range(len(v2)):
        v2[i] = v2[i].split(";")
        for j in range(len(v2[i])):
            # v2[i][j] = v2[i][j].replace(" ","")
            v2[i][j] = v2[i][j].strip()
    # print(v2)
    v2 = v2[:-1]
    dbo.Infoupdate(v2)
    dbo.CVEupdate(v2)
    dbo.close()
    response = JsonResponse({"hello":"hi"})
    return response

def GenMulval(request):
    tom = TM.ToM(tpname)
    tom.GenM(tom.Gettup())
    response = JsonResponse({"hello": "hi"})
    return response
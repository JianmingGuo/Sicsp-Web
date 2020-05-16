from django.shortcuts import render,redirect
import shutil
from nessus import nessus,get_config
from django.shortcuts import HttpResponse
import os


def toMulVAL(req):
    return render(req, "toMulVAL.html")

def tomulvalupload(req):
    shutil.rmtree('./ToMulVAL/upload')
    os.mkdir('./ToMulVAL/upload')
    # print("data: ", req.POST)
    # print("file:", req.FILES)
    if req.method == "POST":
        file = req.FILES.get("upload", None)
        if not file:
            return render(req, "ToMulVAL.html", {"errinf":"No files for upload!"})
        # f = open("./ToMulVAL/upload/test.nessus", 'wb')
        f = open(os.path.join("./ToMulVAL/upload",file.name), 'wb')
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
    file=open('./ToMulval/download/nessus.p','rb')
    response=HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="nessus.p"'
    return response

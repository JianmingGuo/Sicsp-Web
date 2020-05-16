from django.shortcuts import render,redirect
import shutil
from nessus import nessus,get_config
from django.shortcuts import HttpResponse
import os


def toMulVAL(req):
    return render(req, "toMulVAL.html")

def tomulvalupload(req):
    shutil.rmtree('./ToMulVAL/upload')
    # os.mkdir('/root/ICS/mulval/testcases/ns/')
    print("data: ", req.POST)
    print("file:", req.FILES)
    if req.method == "POST":
        file = req.FILES.get("upload", None)
        file.SaveAs()
        if not file:
            return render(req, "ToMulVAL.html", {"errinf":"No files for upload!"})
        f = open("./ToMulVAL/upload/test.nessus", 'wb')
        for line in file.chunks():  # 分块写入
            f.write(line)
        f.close()
    path = "./ToMulVAL/upload/test.nessus"
    nessus(path)

def tomulcaldownload(request):
    file=open('./ToMulval/download/nessus.p','rb')
    response=HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="nessus.p"'
    return response

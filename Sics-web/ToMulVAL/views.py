from django.shortcuts import render,get_object_or_404, redirect, HttpResponse
from blog.models import *
import json
from Sics.utils import *
from django.core.mail import send_mail
from Sics import settings


def toMulVAL(req):
    return render(req, "toMulVAL.html")
import os
from django.shortcuts import render
#from premodel import newscat2pred

def premodel_home(requests):
    cmd = 'python newscat2pred.py'
    os.system(cmd)
    return render(requests, 'testing.html')
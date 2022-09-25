from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
def index(req):
    if req.method == 'POST' and req.FILES['upload']:
        upload = req.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        #VERY INSECURE, ONLY DONE BECAUSE HACKATHON        
        os.system("python3 ./media/aiartist.py ."+ file_url + " &")
        return render(req, 'portraits/index.html', {'file_url': file_url})
    return render(req, 'portraits/index.html')


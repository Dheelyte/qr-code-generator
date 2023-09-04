from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import time
import os

# Create your views here.

class QRGenerator(APIView):

    def get(self, request):
        return render(request, 'core/index.html')
    
    def generate(self, embed_data):
        import qrcode
        
        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=1,
        )
        qr.add_data(embed_data)
        qr.make(fit=True)
        img = qr.make_image()
        name = time.time()
        filepath = os.path.join('media', 'qr', f"{name}.png")
        img.save(filepath)
        fileurl = f"/media/qr/{name}.png"
        return fileurl

    def post(self, request):
        embed_data = request.data.get('embed_data')
        if not embed_data:
            return Response("Enter an information to embed into the QR Code", status=400)
        generated_qr = self.generate(embed_data)
        self.delete_qrs()
        return Response({"generated_qr": generated_qr})

    def delete_qrs(self):
        qr_dir = os.path.join('media', 'qr')
        qrs = os.listdir(qr_dir)
        print(qrs)
        current_time = time.time()
        for qr in qrs:
            qr_location = os.path.join(qr_dir, qr)
            qr_time = os.stat(qr_location).st_mtime
            if (qr_time < current_time - 86400):
                os.remove(qr_location)

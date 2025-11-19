# main/views.py
from django.shortcuts import render  # type: ignore
from django.http import JsonResponse # type: ignore

def index(request):
    """
    Halaman utama -- jika kamu ingin mengakses index langsung di root '/'
    (tergantung urls.py)
    """
    return render(request, 'main/index.html')


def info_page(request):
    """
    Endpoint yang mengembalikan HALAMAN HTML (template).
    Akses: /api/info/  -> akan merender templates/main/index.html
    """
    context = {
        # contoh data yang bisa diakses di template via {{ title }}
        "title": "JELAYAN CAPITAL",
    }
    return render(request, 'main/index.html', context)


def info_api(request):
    """
    Endpoint opsional yang mengembalikan JSON (tetap tersedia di /api/info/json/)
    Jika kamu tidak butuh JSON, boleh hapus fungsi ini dan route yang terkait.
    """
    data = {
        "nim": "221103794",                       # ganti dengan NIM-mu jika perlu
        "nama": "PRESCOBALDI JELAYAN PUTRA",     # ganti dengan nama lengkapmu
    }
    return JsonResponse(data)

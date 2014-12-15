from roxyfileman.utils import Upload, json_response, safepath, ok, err
from django.views.decorators.csrf import csrf_exempt
from roxyfileman.settings import default_settings
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from PIL import Image
import os, shutil


def index(request):
    return render(request, 'roxyfileman/index.html')


def conf(request):
    config = {}
    for key, value in default_settings.items():
        config[key] = getattr(settings, 'ROXY_' + key, value)

    return json_response(config)


@csrf_exempt
def dirlist(request):
    result = []
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        result.append({
            'p': os.path.relpath(root, settings.MEDIA_ROOT),
            'f': len(files), 'd': len(dirs)
        })

    return json_response(result[1:])


@csrf_exempt
def createdir(request):
    path = request.POST.get('d', '')
    name = request.POST.get('n', '')

    if path and name:
        os.makedirs(safepath(settings.MEDIA_ROOT, path, name), exist_ok=True)

    return ok()


@csrf_exempt
def deletedir(request):
    path = request.POST.get('d', '')

    if path:
        shutil.rmtree(safepath(settings.MEDIA_ROOT, path))

    return ok()


@csrf_exempt
def movedir(request):
    path_from = request.POST.get('d', '')
    path_to = request.POST.get('n', '')

    if path_from and path_to:
        shutil.move(
            safepath(settings.MEDIA_ROOT, path_from),
            safepath(settings.MEDIA_ROOT, path_to)
        )

    return ok()


@csrf_exempt
def copydir(request):
    path_from = request.POST.get('d', '')
    path_to = request.POST.get('n', '')

    if path_from and path_to:
        shutil.copytree(
            safepath(settings.MEDIA_ROOT, path_from),
            safepath(settings.MEDIA_ROOT, path_to, os.path.basename(path_from))
        )

    return ok()


@csrf_exempt
def renamedir(request):
    path = request.POST.get('d', '')
    new_name = request.POST.get('n')

    if path and new_name:
        shutil.move(
            safepath(settings.MEDIA_ROOT, path),
            safepath(settings.MEDIA_ROOT, os.path.dirname(path), new_name)
        )

    return ok()


@csrf_exempt
def fileslist(request):
    rel_path = request.GET.get('d', '.')
    full_path = os.path.join(settings.MEDIA_ROOT, rel_path)

    files = []
    for fname in next(os.walk(full_path))[2]:
        files.append({
            'p': safepath(settings.MEDIA_URL, rel_path, fname),
            'w': 0, 'h': 0, 's': 0, 't': 0
        })

    return json_response(files)


@csrf_exempt
def upload(request):
    path = request.POST.get('d', '')
    files = request.FILES.getlist('files[]')

    if path:
        for mfile in files:
            upload = Upload(mfile)
            print(upload.save(path))

    return ok()


@csrf_exempt
def download(request):
    return err()


@csrf_exempt
def deletefile(request):
    path = request.POST.get('d', '')

    if path:
        shutil.rm(safepath(settings.MEDIA_ROOT, path))

    return ok()


@csrf_exempt
def uploaddir(request):
    return err()


@csrf_exempt
def movefile(request):
    path_from = request.POST.get('f', '')
    path_to = request.POST.get('n', '')

    if path_from and path_to:
        path_from = path_from.replace(settings.MEDIA_URL, )

        shutil.move(
            safepath(settings.MEDIA_ROOT, path_from),
            safepath(settings.MEDIA_ROOT, path_to)
        )

    return ok()


@csrf_exempt
def copyfile(request):
    path_from = request.POST.get('d', '')
    path_to = request.POST.get('n', '')

    if path_from and path_to:
        shutil.copy(
            safepath(settings.MEDIA_ROOT, path_from),
            safepath(settings.MEDIA_ROOT, path_to, os.path.basename(path_from))
        )

    return ok()


@csrf_exempt
def renamefile(request):
    path = request.POST.get('d', '')
    new_name = request.POST.get('n')

    if path and new_name:
        shutil.move(
            safepath(settings.MEDIA_ROOT, path),
            safepath(settings.MEDIA_ROOT, os.path.dirname(path), new_name)
        )

    return ok()


@csrf_exempt
def thumb(request):
    path = request.GET.get('f', '')
    width = request.GET.get('w', 100)
    height = request.GET.get('h', 100)

    if path:
        response = HttpResponse(content_type='image/jpeg')
        image = Image.open(safepath(settings.BASE_DIR, path))
        image.thumbnail((width, height))
        image.save(response, 'JPEG')
        return response

    return err()

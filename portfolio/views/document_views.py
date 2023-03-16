from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from portfolio.models import Document
from django.shortcuts import render, redirect

import os


# Render the document upload page.
@login_required
def document_upload(request, company_id):
    return render(request, "document/document_upload.html", {"company_id": company_id})


# Redirect to an external document.
@login_required
def open_url(request, file_id):
    document = Document.objects.get(file_id=file_id)
    document_url = document.url

    return redirect(document_url)


# Download a document from the database.
@login_required
def download_document(request, file_id):
    document = Document.objects.get(file_id=file_id)
    file_path = document.file.path

    if os.path.exists(file_path):
        with open(file_path, "rb") as download_file:
            response = HttpResponse(download_file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + document.file_name
            return response
    else:
        raise Http404


# Delete a document from the database.
@login_required
def delete_document(request, file_id):
    document = Document.objects.get(file_id=file_id)

    try:
        document.delete()
    except Document.DoesNotExist:
        print("Document does not exist.")

    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from portfolio.forms import DocumentUploadForm, URLUploadForm
from portfolio.models import Document

import os


# Render the document upload page.
@login_required
def document_upload(request, company_id):
    if request.method == "POST":
        if "upload_file" in request.POST:
            form = DocumentUploadForm(request.POST, request.FILES)

            if form.is_valid():
                new_document = form.save(commit=False)
                new_document.company_id = company_id
                new_document.save()
                return redirect("portfolio_company", company_id=company_id)

        elif "upload_url" in request.POST:
            form = URLUploadForm(request.POST)

            if form.is_valid():
                new_document = form.save(commit=False)
                new_document.company_id = company_id
                new_document.save()
                return redirect("portfolio_company", company_id=company_id)
    else:
        file_form = DocumentUploadForm()
        url_form = URLUploadForm()

        context = {
            "file_form": file_form,
            "url_form": url_form,
            "company_id": company_id
        }

    return render(request, "document/document_upload.html", context)


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
            response = HttpResponse(download_file.read(), content_type="application/octet-stream")
            response["Content-Disposition"] = "attachment; filename=" + document.file_name

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

    return redirect(request.META.get("HTTP_REFERER", "/"))

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Render the document upload page.
@login_required
def document_upload(request):
    return render(request, "document/document_upload.html")

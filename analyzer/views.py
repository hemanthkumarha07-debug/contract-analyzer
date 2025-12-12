from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text, analyze_contract

def analyze_view(request):
    analysis = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            raw_text = extract_text(request.FILES['file'])
            analysis = analyze_contract(raw_text)
    else:
        form = UploadFileForm()

    return render(request, 'analyze.html', {'form': form, 'result': analysis})
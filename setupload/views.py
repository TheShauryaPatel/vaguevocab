from io import StringIO

import pandas as pd
from django.shortcuts import render, redirect

from .forms import CsvUploadForm, CsvPasteForm


def upload_csv(request):
    form = CsvUploadForm(request.POST, request.FILES)
    form2 = CsvPasteForm(request.POST, request.FILES)

    if request.method == 'POST':
        if 'form1_submit' in request.POST and form.is_valid():  # Check if Form 1 is submitted
            print('form 1 represent')
            csv_files = request.FILES.getlist('csv_files')  # Get the list of uploaded files
            quantity = form.cleaned_data['number_input']

            column_names = ['FRONT', 'BACK']  # Replace with your column names
            dataframes = [pd.read_csv(file, sep='\t', header=None, names=column_names) for file in csv_files]

            sheet = pd.concat(dataframes, ignore_index=True)
            items = sheet.sample(n=quantity)
            items_json = items.to_json(orient='split')

            request.session['dataframe'] = items_json
            return redirect('main:quizscreen:quiz')

        elif 'form2_submit' in request.POST and form2.is_valid():  # Check if Form 2 is submitted
            csv_text = form2.cleaned_data['csv_text']
            quantity = form2.cleaned_data['number_input']

            column_names = ['FRONT', 'BACK']
            csv_data = StringIO(csv_text)
            dataframes = [pd.read_csv(csv_data, sep='\t', header=None, names=column_names)]

            sheet = pd.concat(dataframes, ignore_index=True)
            items = sheet.sample(n=quantity)
            items_json = items.to_json(orient='split')

            request.session['dataframe'] = items_json
            return redirect('main:quizscreen:quiz')

    else:
        form = CsvUploadForm()
        form2 = CsvPasteForm()

    return render(request, 'setupload/upload.html', {'form': form, 'form2': form2})

import pickle
import pandas as pd

from django.shortcuts import render


def quiz(request):
    # Retrieve dataframe from session
    items_json = request.session.get('dataframe')

    # If the session data exists, convert it back to a dataframe
    if items_json:
        items = pd.read_json(items_json, orient='split')

        # Extract 'front' column values
        front_values = items['FRONT'].tolist()
        quantity = len(front_values)
        return render(request, 'quizscreen/output.html', {'front_values': front_values, 'quantity':quantity})

    else:
        return render(request, 'quizscreen/output.html', {'error': ['No data available']})
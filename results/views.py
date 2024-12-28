import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from .simfuncs import *


def result(request):
    if request.method == 'POST':
        # Extract submitted data
        items_json = request.session.get('dataframe')
        items = pd.read_json(items_json, orient='split')
        fronts = items['FRONT']
        backs = items['BACK']
        responses = {key: value for key, value in request.POST.items() if key.startswith('responses_')}
        answers_given = list(zip([key.split('_')[1] for key in responses.keys()], fronts, backs, responses.values()))
        results = []
        for i in range(len(answers_given)):
            embedding1 = model.encode(answers_given[i][2], convert_to_tensor=True)
            embedding2 = model.encode(answers_given[i][3], convert_to_tensor=True)
            accuracy, truth = similarity_tester(embedding1, embedding2)
            results.append((
                answers_given[i][0],
                answers_given[i][1],
                answers_given[i][2],
                answers_given[i][3],
                int(accuracy * 100),
                int(100 - (accuracy * 100)),
                f'{['Wrong', 'Correct'][truth]}',
                f'{['#520c70', '#4caf50'][truth]}',
            )
            )
        # Process the data as needed
        # Pass results to the results page
        return render(request, 'results/results.html', {'results': results})
    return HttpResponse("Invalid request", status=400)

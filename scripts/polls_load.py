import csv  # https://docs.python.org/3/library/csv.html

import datetime
from django.utils import timezone

from polls.models import Question, Choice

def run():
    print("=== Polls Loader")

    Choice.objects.all().delete()
    Question.objects.all().delete()
    print("=== Objects deleted")

    fhand = open('scripts/dj4e_batch.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    for row in reader:
        print(row)

        # Skip lines without a question and at least one choice
        if len(row) < 2:
            continue

        # Make a new Question and save it
        q = Question(question_text=row[0], pub_date=timezone.now())
        q.save()

        # Loop through the choice strings in row[1:] and add each choice,
        # connect it to the question and save it
        for choice_text in row[1:]:
            c = Choice(question=q, choice_text=choice_text, votes=0)
            c.save()

    fhand.close()
    print("=== Load Complete")

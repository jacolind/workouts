import typeform

apikey = '07466391d081290e87a95868893868e6e55c73c3' #my account
formid = 'xqBhCO' #my training data form

form = typeform.Form(api_key=apikey, form_id=formid)

## Fetch all responses to the form with default options
responses = form.get_responses()

## Fetch responses with specific options
response_limit =2 10 #change this one?
since_time = 1487863154 #qq what is this?
responses = form.get_responses(limit=response_limit, since=since_time)

## Print '<question>: <answer>' for all responses to this form
for response in responses:
    for answer in response.answers:
        print '{question}: {answer}'.format(question = answer.question,
                                            answer = answer.answer)

## Fetch a specific response
#qq ve tej vad denna gör
#response = form.get_response('<response_token>')

######################### version 2

import typeform

# set my parameters and download the form data
apikey = '07466391d081290e87a95868893868e6e55c73c3'
formid = 'xqBhCO'
form = typeform.Form(api_key=apikey, form_id=formid)

# Fetch all responses to the form with default options
responses = form.get_responses()
responses # I have 16 questions and 138 responses

# Print '<question>: <answer>' for all responses to this form
for response in responses:
    for answer in response.answers:
        print '{question}: {answer}'.format(question=answer.question, answer=answer.answer)

The last call gives output:

    >>> for response in responses:
    ...     for answer in response.answers:
    ...         print '{question}: {answer}'.format(question=answer.question, answer=answer.answer)
    ...
    Yoga: 1
    date: 2017-11-10
    Traceback (most recent call last):
      File "<stdin>", line 3, in <module>
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xe5' in position 10: ordinal not in range(128)

# put them in a dictionary
dict = []
for r in responses:
    for a in r.answers:
        print '{question}: {answer}'.format(question=a.question, answer=a.a)
        dict.append()


# Fetch a specific response
response = form.get_response('<response_token>')

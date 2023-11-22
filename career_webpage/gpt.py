from json import dumps

from openai import OpenAI


def call_gpt_generate_cv(user_data):
    client = OpenAI()

    json = dumps(user_data)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content":
                    "You are an expert professional document writer."
                    "The user will provide you with a list of their professional experiences, previous jobs, titles."
                    "User input will be specified in JSON format."
                    "Please, write a few hundred words CV for the user in markdown format."
                    "Make it as professional as possible."
            }, {
                  "role": "user",
                  "content": json
            }
        ]
    )

    return completion.choices[0].message.content


def call_gpt_generate_cl(user_data, job_description):
    client = OpenAI()

    data = user_data
    data.update(job_description)

    json = dumps(data)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content":
                    "You are an expert professional document writer."
                    "The user will provide you with a list of their professional experiences, previous jobs, titles."
                    "The user will also provide a short description of the job they are applying for."
                    "User input will be specified in JSON format."
                    "Please, write a one-page cover letter for the specified job in markdown format."
            }, {
                "role": "user",
                "content": json
            }
        ]
    )

    return completion.choices[0].message.content



def call_gpt_generate_advice(user_data):
    client = OpenAI()

    json = dumps(user_data)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content":
                    "You are an expert career advisor."
                    "The user will provide you with a list of their professional experiences, previous jobs, titles."
                    "User input will be specified in JSON format."
                    "Please, write a short, detailed text giving the user some advice to take their career to the next level."
                    "Use MarkDown format."
            }, {
                "role": "user",
                "content": json
            }
        ]
    )

    return completion.choices[0].message.content
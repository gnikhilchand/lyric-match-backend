# from openai import OpenAI

# client = OpenAI(
#     api_key="sk-76a199dc64b1459f9974360252c73f41",
#     base_url="https://api.deepseek.com"
# )

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Generate 2-4 lines of lyrics from the song 'Bohemian Rhapsody' without revealing the song title."},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)

# from openai import OpenAI

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key="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",
# )

# completion = client.chat.completions.create(
#   extra_headers={
#     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#   },
#   model="deepseek/deepseek-r1:free",
#   messages=[
#     {
#       "role": "user",
#       "content": "What is the meaning of life?"
#     }
#   ]
# )
# print(completion.choices[0].message.content)

# import requests
# import json

# response = requests.post(
#   url="https://openrouter.ai/api/v1/chat/completions",
#   headers={
#     "Authorization": "<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>",
#     "Content-Type": "application/json",
#     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#   },
#   data=json.dumps({
#     "model": "deepseek/deepseek-r1-zero:free",
#     "messages": [
#       {
#         "role": "user",
#         "content": "What is the meaning of life?"
#       }
#     ],
    
#   })
# )
#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
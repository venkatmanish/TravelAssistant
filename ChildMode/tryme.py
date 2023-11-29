import os
import openai

openai.api_key = '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'
response = openai.Image.create(prompt="a white siamese cat",
                               n=1,
                               size="1024x1024")
image_url = response['data'][0]['url']
print(image_url)
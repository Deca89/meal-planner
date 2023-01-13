import openai

openai.api_key = "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"

prompt = "can you give me a vegan recipe in dynamodb format with metric instructions?"

completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

message = completions.choices[0].text
print(message)

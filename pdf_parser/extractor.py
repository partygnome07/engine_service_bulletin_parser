import json
from openai import OpenAI

def call_extraction(text: str, function_schema: dict, client: OpenAI) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a PDF data extractor."},
            {"role": "user", "content": text}
        ],
        functions=[function_schema],
        function_call={"name": function_schema["name"]}
    )
    raw_args = response.choices[0].message.function_call.arguments
    try:
        return json.loads(raw_args)
    except Exception as e:
        raise ValueError(f"❌ Failed to parse function output: {raw_args}") from e

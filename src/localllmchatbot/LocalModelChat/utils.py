# handles stream response back from LLM
def stream_parser(stream):
    for chunk in stream:
        yield chunk['message']['content']
import tiktoken
encoding = tiktoken.encoding_for_model('gpt-4o-mini')  # o200k_base
print(encoding)
tokenizer = tiktoken.get_encoding("o200k_base")
print(tokenizer)
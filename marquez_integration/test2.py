import os
import re
from openai import OpenAI

msg = f"""SQL Code: ```select * from user_table```
requirements:
1. Give the result in the Json format. Only conside tables that already exist in DB or saved to DB finally.
'tables': a list of tables. These tables already exist in DB, and their rows are not changed. Use comma to seperate the tables.
2. Give the json result only.
"""
try:
    client = OpenAI(
        api_key="abcdefghijklmn",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="llm_model",
        messages=[
            {'role': 'system',
             'content': 'You are a SQL expert. Given a Spark SQL code, please help user to list tables used in the code'},
            {'role': 'user', 'content': msg}],
    )
    pattern = r'```json(.*?)```'

    matches = re.findall(pattern, completion.choices[0].message.content, re.DOTALL)
    print({'result': matches[0]})
except Exception as e:
    # This block will execute if an error occurs in the try block
    print(f"An error occurred: {e}")
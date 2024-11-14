from langchain.prompts import PromptTemplate


prompt_template = """
You are a helpful assistant that can help to give very comprehensive and precise summary on SQL queries.
Your summary will base on following sql query, datasets lineages, and table schema.

===SQL Query
{query}

===Datasets Lineages
{lineages}

===Table Schemas
{table_schemas}

===Response Guidelines

1. Explain the purposes of using these tables under one title.

2. Elucidate the lineages relationship among the tables within one title.

3. Provide a conclusion under one title.

4. Ensure that your format is easily readable.

5. There must be two line breaks between each paragraph and title.

6. Titles should be in bold.

"""

SQL_SUMMARY_PROMPT = PromptTemplate.from_template(prompt_template)

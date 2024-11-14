from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import DashVector

from lib.vector_store.stores.opensearch import OpenSearchVectorStore

ALL_PLUGIN_VECTOR_STORES = {"opensearch": OpenSearchVectorStore}
ALL_PLUGIN_EMBEDDINGS = {"dashscope": DashScopeEmbeddings}

# Example to add vector store

# from lib.vector_store.stores.opensearch import OpenSearchVectorStore
# from langchain.embeddings import OpenAIEmbeddings

# ALL_PLUGIN_VECTOR_STORES = {"opensearch": OpenSearchVectorStore}
# ALL_PLUGIN_EMBEDDINGS = {"openai": OpenAIEmbeddings}

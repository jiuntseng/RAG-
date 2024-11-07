import getpass
import os

os.environ["OPENAI_API_KEY"] = "insert key here"
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader

path = "Frankenstein.txt"
loader = TextLoader(path)
pages = loader.load_and_split()

#from langchain_text_splitters import RecursiveCharacterTextSplitter

#text_splitter = RecursiveCharacterTextSplitter(
#    chunk_size=1000, chunk_overlap=200, add_start_index=True)
#all_splits = text_splitter.split_documents(pages)

#len(all_splits)

vectorstore = Chroma.from_documents(documents=pages, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

from langchain import hub

# setting environmental variables for observability purposes
# according to https://smith.langchain.com/onboarding?organizationId=c442aa62-b658-4078-96dc-d9a33c9a737a&step=1
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "RAG_littlewomen"

prompt = hub.pull("rlm/rag-prompt")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

llm = model
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for chunk in rag_chain.stream("who am I speaking to?"):
    print(chunk, end="", flush=True)


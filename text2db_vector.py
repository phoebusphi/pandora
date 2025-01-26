import os
import time
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
load_dotenv()

from pinecone import Pinecone, ServerlessSpec
os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

openai_ef = embedding_functions.OpenAIEmbeddingFunction("",
                                                        model_name="text-embedding-3-large"
                                                        )
os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_TYPE")
def upload_dbvector():
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")
    path_folder_main = "./markdown_files/"
    folder_main = os.listdir(path_folder_main)
    namespace = os.getenv("NAMESPACE_PINECONE")
    index = os.getenv("INDEX_PINECONE")
    c=0
    total = 0


    for folder in folder_main:
        files = os.listdir(path_folder_main + folder+"/")
        print(folder)
        for file in files:
            print(file)
            loader = TextLoader(path_folder_main + folder +"/"+file,
                                encoding="utf-8")
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=3500, chunk_overlap=0)
            doc = text_splitter.split_documents(documents)
            for text in doc:
                text.metadata["source"] = "documents/{}.md".format(folder +"_"+file)
                text.metadata["archivo"] = folder
                text.metadata["page"] = file.split(".")[0].split("-")[-1]
                text.metadata["type_document"] = "norm"
            docsearch = PineconeVectorStore.from_documents(
                documents=doc,
                index_name=index,
                embedding=embeddings_model,
                namespace=namespace
            )
            c+=1
            print("Documento procesado {} y pagina {}".format(folder, file))
            time.sleep(1)
        time.sleep(1)

# @Kelly @Fernando
import os
import openai
import warnings
import PyPDF2
import ast
import random as rd
import warnings
from PyPDF2 import PdfWriter, PdfReader
from langchain_community.chat_models import ChatOpenAI
import openai
from llama_parse import LlamaParse
import nltk
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfWriter, PdfReader
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

# path = os.getcwd()
# load_dotenv()

### se queda
def check_folder(name_folder:str, delete=False):
    a = os.getcwd()
    a = a.replace('\\', '/')
    path = a + '/' + name_folder
    try:
        os.makedirs(path)
        print("folder created")
    except:
        # if name_folder in os.listdir(a):
        print("folder already exists")
        if delete is True:
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
        else:
            pass


parser = LlamaParse(
    api_key="",
    result_type="markdown",
    num_workers=4,
    verbose=True,
    language="en",
)

def split_pdf(name,folder):
    pdf_file1 = PdfReader(open(name, 'rb'))
    num_page = len(pdf_file1.pages)
    new_folder = folder
    path = os.getcwd() + "\\" + new_folder
    path = path.replace('\\', '/')
    check_folder(new_folder)
    for page_num in range(num_page):
        pdf_writer = PdfWriter()
        page = pdf_file1.pages[page_num]
        pdf_writer.add_page(page)
        with open("{}/{}.pdf".format(path,str(page_num)), "wb") as outputStream:
            pdf_writer.write(outputStream)

def process_page(page, path_md, path_page=None):
    name_page = page.split('.')[0]
    markdown_content = parser.load_data(path_page+page)  # Convert to Markdown
    text_markdown_content = markdown_content[0].dict().get('text')
    #markdown folder
    new_folder = "markdown_files"
    path = os.getcwd() + "\\" + new_folder+"\\"+path_md
    path = path.replace('\\', '/')
    # check_folder(path_md)
    with open("{}/{}.md".format(path,name_page), 'w', encoding='utf-8') as f:
        f.write(text_markdown_content)

def main_pdf2md(path="./documentation"):
    l = os.listdir(path)
    for file in l:
        folder_name = file.split(".")[0]
        print(folder_name)
        os.makedirs("./pdf_files/{}".format(folder_name))
        split_pdf("./documentation/"+file, folder_name)
        for f in os.listdir("./pdf_files/{}".format(folder_name)):
            process_page(f, folder_name, path_page="./pdf_files/{}/".format(folder_name))

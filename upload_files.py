from task import main_pdf2md
from text2db_vector import upload_dbvector

main_pdf2md() ## split and convert pdf to markdown
upload_dbvector() ## upload markdown files to pinecone

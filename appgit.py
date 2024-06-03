from flask import Flask, request, render_template
import os
from docx import Document
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)

huggingfacehub_api_token = os.environ["HUGGINGFACE_EDU"]

prompt_template = """
You are an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. Below is some information. 
{context}

Based on the above information only, answer the below question. 

{question}
"""

prompt = PromptTemplate.from_template(prompt_template)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            content = uploaded_file.read().decode('utf-8')
            file_path = "temp/file.txt"
            write_text_file(content, file_path)
            loader = TextLoader(file_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=256, chunk_overlap=0, separators=[" ", ",", "\n", "."]
            )
            texts = text_splitter.split_documents(docs)
            embeddings = HuggingFaceEmbeddings()
            db = Chroma.from_documents(texts, embeddings)
            question = request.form['question']
            similar_doc = db.similarity_search(question, k=1)
            context = similar_doc[0].page_content
            llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token, 
                                 repo_id="tiiuae/falcon-7b-instruct", 
                                 model_kwargs={"temperature":0.6, "max_new_tokens":500})
            query_llm = LLMChain(llm=llm, prompt=prompt)
            response = query_llm.run({"context": context, "question": question})
            return render_template('index.html', response=response)
    return render_template('index.html')

def write_text_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error occurred while writing the file: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)

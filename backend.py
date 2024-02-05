from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import NLTKTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import SpacyTextSplitter
#from vertexai.language_models import TextEmbeddingModel
from bs4 import BeautifulSoup
import re
from langchain.docstore.document import Document


# Load pdf data with PyPDFLoader
def read_pdf(pdf_file):
    loader = PyPDFLoader(pdf_file)
    pages = loader.load_and_split(text_splitter_nltk)
    return pages

# Load pdf data with PDFMinerPDFasHTMLLoader generates HTML from PDF for semantic parsing.
def read_pdf_to_html(pdf_file):
    loader = PDFMinerPDFasHTMLLoader(pdf_file)
    data = loader.load_and_split(text_splitter)
    
    soup = BeautifulSoup(data,'html.parser')
    #content = soup.find_all('div')
    print(content)
    quit()
    cur_fs = None
    cur_text = ''
    snippets = []   # first collect all snippets that have the same font size
    for c in content:
        sp = c.find('span')
        if not sp:
            continue
        st = sp.get('style')
        if not st:
            continue
        fs = re.findall('font-size:(\d+)px',st)
        if not fs:
            continue
        fs = int(fs[0])
        if not cur_fs:
            cur_fs = fs
        if fs == cur_fs:
            cur_text += c.text
        else:
            snippets.append((cur_text,cur_fs))
            cur_fs = fs
            cur_text = c.text
    snippets.append((cur_text,cur_fs))

    cur_idx = -1
    semantic_snippets = []
    # Assumption: headings have higher font size than their respective content
    for s in snippets:
        # if current snippet's font size > previous section's heading => it is a new heading
        if not semantic_snippets or s[1] > semantic_snippets[cur_idx].metadata['heading_font']:
            metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
            metadata.update(data.metadata)
            semantic_snippets.append(Document(page_content='',metadata=metadata))
            cur_idx += 1
            continue

        # if current snippet's font size <= previous section's content => content belongs to the same section (one can also create
        # a tree like structure for sub sections if needed but that may require some more thinking and may be data specific)
        if not semantic_snippets[cur_idx].metadata['content_font'] or s[1] <= semantic_snippets[cur_idx].metadata['content_font']:
            semantic_snippets[cur_idx].page_content += s[0]
            semantic_snippets[cur_idx].metadata['content_font'] = max(s[1], semantic_snippets[cur_idx].metadata['content_font'])
            continue

        # if current snippet's font size > previous section's content but less than previous section's heading than also make a new
        # section (e.g. title of a PDF will have the highest font size but we don't want it to subsume all sections)
        metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
        metadata.update(data.metadata)
        semantic_snippets.append(Document(page_content='',metadata=metadata))
        cur_idx += 1
    return semantic_snippets

# Embed PDF
def chunk_data(data):
    text_splitter = NLTKTextSplitter()
    docs = text_splitter.split_text(text)



if __name__ == "__main__":
    # Read PDF
    pdf_file="sample-docs/cost-opt-best-practice.pdf"

    # Splitters
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False)
    
    #text_splitter2 = SpacyTextSplitter(chunk_size=1000)
    
    text_splitter_nltk = NLTKTextSplitter()
    text_splitter_sentence = sentence

    # Read PDF
    data = read_pdf(pdf_file)

    print(data[0])
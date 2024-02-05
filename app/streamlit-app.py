import streamlit as st 

def main():
    st.set_page_config(page_title="RAG Demo w/ PDF")
    
    st.header("TechSummit 24 Demo")
    demo_mode = st.checkbox("RAG Demo Mode", value=False)

    st.text_input("Ask me a question", key="question")
    if demo_mode:    
        st.subheader("Code", divider='rainbow')
        st.caption("Loading Code")
        loader_code = '''
            import PyPDF2
            def load_pdf_data(pdf_file_path):
                text = ''
                with open(pdf_file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + ' '  # Concatenating text from each page
                return text
                '''
        st.code(loader_code, language='python')        
        st.caption("Chunking Code")
        chunking_code = '''
        text = "..." # your text
    from langchain.text_splitter import NLTKTextSplitter
    text_splitter = NLTKTextSplitter()
    docs = text_splitter.split_text(text)

                '''
        st.code(chunking_code, language='python')  
        st.caption("Emedding Code")
        embedding_code = '''
        from vertexai.language_models import TextEmbeddingModel


    def text_embedding(data) -> list:
        """Text embedding with a Large Language Model."""
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        embeddings = model.get_embeddings(data)
        for embedding in embeddings:
            vector = embedding.values
            print({len(vector)}")
        return vector

                ''' 
        st.code(embedding_code, language='python')  
    with st.sidebar:
        if demo_mode: 
            st.subheader("Configurations")
            st.file_uploader("Upload PDF")
            
            pdf_loader = st.selectbox(
                'Select a Document Loader',
                ('PyPDFLoader', 'PDFMinerPDFasHTMLLoader'))
            
            text_splitter = st.selectbox(
                'Select a Text Splitter',
                ('RecursiveCharacterTextSplitter', 'NLTKTextSplitter', 'SpacyTextSplitter'))
            
            chunk_size = st.number_input('Chunksize',min_value=10, max_value=1000, value=100)

            chunk_overlap = st.number_input(
                min_value=1,
                max_value=chunk_size - 1,
                label="Chunk Overlap",
                value=int(chunk_size * 0.2),
            )

            # Display a warning if chunk_overlap is not less than chunk_size
            if chunk_overlap >= chunk_size:
                st.warning("Chunk Overlap should be less than Chunk Length!")

            st.button("Process PDF")
           

if __name__ == "__main__":
    main()

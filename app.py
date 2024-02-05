import streamlit as st 

def main():
    st.set_page_config(page_title="RAG Demo w/ PDF")
    
    st.header("RAG Demo w/ PDF")
    st.text_input("Ask me a question about RAG", key="question")

    with st.sidebar:
        st.subheader("My Documents")
        st.file_uploader("Upload PDF"))
        st.button("Upload")



if __name__ == "__main__":
    main()

import streamlit as st

#st.set_page_config(page_title="My Webpage", layout="wide")
nuval = 20
with st.container():
    #st.subheader("Answer Script Anomaly Detection")
    st.title("Answersheet Anomaly Detection")
    
with st.container():

    st.markdown('## Flowchart of Proposed Solution')
    
    st.image("views/flowchart.jpeg", caption="Flowchart of Proposed Solution")

    st.markdown('## Workflow for Similarity Calculation')

    st.image("views/workflow.jpeg", caption="Workflow for Similarity Calculation")

    st.markdown('## LP techniques used -')
    st.write('1. Tokenization (for sentences and words).')

    st.write('2. Stopword Removal : Removing commonly used words (e.g., "the," "and," "is") that don’t carry significant meaning for analysis.')

    st.write('3. Part-of-Speech (POS) Tagging : Assigning grammatical labels (e.g., noun, verb, adjective) to each word.')
    #st.write('use ;  To extract the proportions of nouns, verbs, and adjectives in the text, which are used as features for stylistic analysis.')

    st.write('4. Lexical Diversity Calculation: Measuring the ratio of unique words to the total number of words.') 
    #st.write('use : evaluate the variety of vocabulary in the text, which can indicate stylistic patterns.')

    st.write('5. Readability Score Approximation : Estimating how easy or difficult a text is to read.')
    #st.write('use : To quantify the complexity of the text.')

    st.write('6. Content Word Analysis :  Calculating the proportions of different types of content words (nouns, verbs, adjectives). use : To identify stylistic differences based on word usage patterns.')

    st.write('7. Cosine Similarity :  A mathematical technique to measure the similarity between two feature vectors (in this case, representing the PDFs). use : To determine how closely related two documents are in terms of their linguistic and stylistic features.')
            


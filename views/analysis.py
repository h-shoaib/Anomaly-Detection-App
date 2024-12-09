import streamlit as st
import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import pandas as pd


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to preprocess text and extract features
def extract_features(text):
    # Process the text with spaCy
    doc = nlp(text.lower())
    
    # Tokenize sentences
    sentences = list(doc.sents)
    sentence_count = len(sentences)

    # Tokenize words and remove stopwords
    words_filtered = [token.text for token in doc if token.is_alpha and not token.is_stop]
    
    # Calculate lexical diversity
    lexical_diversity = len(set(words_filtered)) / len(words_filtered) if len(words_filtered) > 0 else 0
    
    # Calculate average sentence length
    avg_sentence_length = len(words_filtered) / sentence_count if sentence_count > 0 else 0
    
    # Part-of-speech tagging to get noun, verb, adjective counts
    noun_count = sum(1 for token in doc if token.pos_ == 'NOUN')
    verb_count = sum(1 for token in doc if token.pos_ == 'VERB')
    adj_count = sum(1 for token in doc if token.pos_ == 'ADJ')
    
    # Total count of content words
    total_content_words = len(words_filtered)
    
    # Calculate percentage of nouns, verbs, and adjectives
    noun_percentage = noun_count / total_content_words if total_content_words > 0 else 0
    verb_percentage = verb_count / total_content_words if total_content_words > 0 else 0
    adj_percentage = adj_count / total_content_words if total_content_words > 0 else 0
    other_percentage = 1 - (noun_percentage + verb_percentage + adj_percentage)
    
    # Readability score (using average sentence length and average token length)
    syllables_per_word = np.mean([len(token) for token in words_filtered])  # Approximation of syllables per word
    readability_score = avg_sentence_length * syllables_per_word
    
    # Return all features in a dictionary
    features = {
        'readability_score': readability_score,
        'lexical_diversity': lexical_diversity,
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'noun_percentage': noun_percentage,
        'verb_percentage': verb_percentage,
        'adj_percentage': adj_percentage,
        'other_percentage': other_percentage
    }
    
    return features

# Hardcoded feature data for pdf1, pdf2, pdf3 (same as in the previous step)
pdf_features = {
    'pdf1': {
        'readability_score': 14.8,
        'lexical_diversity': 0.72,
        'sentence_count': 32,
        'avg_sentence_length': 18.4,
        'noun_percentage': 0.40,
        'verb_percentage': 0.22,
        'adj_percentage': 0.16,
        'other_percentage': 0.22
    },
    'pdf2': {
        'readability_score': 13.5,
        'lexical_diversity': 0.68,
        'sentence_count': 28,
        'avg_sentence_length': 20.2,
        'noun_percentage': 0.35,
        'verb_percentage': 0.25,
        'adj_percentage': 0.20,
        'other_percentage': 0.20
    },
    'pdf3': {
        'readability_score': 12.5,
        'lexical_diversity': 0.56,
        'sentence_count': 45,
        'avg_sentence_length': 15.3,
        'noun_percentage': 0.38,
        'verb_percentage': 0.30,
        'adj_percentage': 0.22,
        'other_percentage': 0.10
    }
}

# Function to calculate similarity between two PDFs
def calculate_similarity(pdf1_features, pdf2_features):
    # Extract features into arrays for comparison
    features1 = np.array([
        pdf1_features['readability_score'],
        pdf1_features['lexical_diversity'],
        pdf1_features['sentence_count'],
        pdf1_features['avg_sentence_length'],
        pdf1_features['noun_percentage'],
        pdf1_features['verb_percentage'],
        pdf1_features['adj_percentage'],
        pdf1_features['other_percentage']
    ]).reshape(1, -1)

    features2 = np.array([
        pdf2_features['readability_score'],
        pdf2_features['lexical_diversity'],
        pdf2_features['sentence_count'],
        pdf2_features['avg_sentence_length'],
        pdf2_features['noun_percentage'],
        pdf2_features['verb_percentage'],
        pdf2_features['adj_percentage'],
        pdf2_features['other_percentage']
    ]).reshape(1, -1)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(features1, features2)
    return similarity[0][0]

# Function to compare pdf4 with pdf1, pdf2, and pdf3
def compare_with_existing_pdfs(pdf4_text, pdf_features):
    # Extract features for pdf4
    pdf4_features = extract_features(pdf4_text)
    
    results = {}
    for pdf_name, features in pdf_features.items():
        similarity_score = calculate_similarity(pdf4_features, features)
        results[pdf_name] = similarity_score
    return results

# Input the raw text for pdf4
pdf4_text = st.session_state['semtext']

# Compare pdf4 with pdf1, pdf2, and pdf3
similarity_results = compare_with_existing_pdfs(pdf4_text, pdf_features)
df = pd.DataFrame(similarity_results.items(), columns=['Compared To', 'Similarity'])
# Display the results
#print("Similarity results for pdf4:")
#for pdf_name, similarity_score in similarity_results.items():
#    print(f"Similarity with {pdf_name}: {similarity_score:.2f}")

# Determine likelihood of similar authors
threshold = 0.8  # A threshold to decide if the documents are by the same author
#for pdf_name, similarity_score in similarity_results.items():
#    if similarity_score > threshold:
#        print(f"Likelihood of similar authors: High for {pdf_name}")
#    else:
#        print(f"Likelihood of similar authors: Low for {pdf_name}")
if 'semtext' not in st.session_state:
    st.markdown("# UPLOAD FILE FOR ANALYSIS ")

if 'semtext' in st.session_state:
    txt = st.session_state.semtext
    #result = anomaly_detection(txt)

    with st.container():
        #st.subheader("Answer Script Anomaly Detection")
        st.markdown("## Similarity values for uploaded doc:")
        st.write('---')
        st.data_editor(
            df,
            column_config={
                "Similarity": st.column_config.ProgressColumn(
                    "Similarity compared to other pdf files",
                    format="%.2f",
                    min_value=0,
                    max_value=1,
                    ),
                },
            hide_index=True,
        )
        st.write('---')
        for pdf_name, similarity_score in similarity_results.items():
            html_str = f"""
                <style>
                p.a {{
                font: bold 20px Courier;
                }}
                </style>
                <p class="a">Similarity with {pdf_name}: {similarity_score:.2f}</p>
                """
            st.markdown(html_str, unsafe_allow_html=True)
            
            #st.markdown(f"Similarity with {pdf_name}: {similarity_score:.2f}")
        st.write('---')    
        st.markdown("## Interpretation")
        st.write('--')
        for pdf_name, similarity_score in similarity_results.items():
            
            if similarity_score > threshold:
                html_str = f"""
                <style>
                p.a {{
                font: bold 20px Courier;
                }}
                </style>
                <p class="a">Likelihood of similar authors: High for {pdf_name}</p>
                """
                st.markdown(html_str, unsafe_allow_html=True)
                #st.markdown(f"##Likelihood of similar authors: High for {pdf_name}")
            else:
                html_str = f"""
                <style>
                p.a {{
                font: bold 20px Courier;
                }}
                </style>
                <p class="a">Likelihood of similar authors: Low for {pdf_name}</p>
                """
                st.markdown(html_str, unsafe_allow_html=True)
                #st.markdown(f"##Likelihood of similar authors: Low for {pdf_name}")
        #st.write(f"Likelihood of Multiple Authors: {result['Likelihood_Multiple_Authors']}%")
        #st.write(f"Lexical Diversity: {result['Lexical_Diversity']:.2f}")
        #st.write(f"Average Semantic Similarity: {result['Average_Semantic_Similarity']:.2f}")
        #st.write(f"Number of Clusters Detected: {result['Number_of_Clusters']}\n")

        #col1, col2, col3, col4 = st.columns(4)
        #st.metric("Likelihood of Multiple Authors", f"{result['Likelihood_Multiple_Authors']}%")
        #st.metric("Lexical Diversity", f"{result['Lexical_Diversity']:.2f}")
        #st.metric("Avg Semantic Similarity", f"{result['Average_Semantic_Similarity']:.2f}")
        #st.metric("No. of Clusters Detected", f"{result['Number_of_Clusters']}")
import streamlit as st

#st.set_page_config(page_title="My Webpage", layout="wide")

with st.container():
    st.subheader("Answer Script Anomaly Detection")
    st.title("Software to detect cheating in handwritten answer scripts")
    
with st.container():
    #st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What this software does:")
        #st.write("##")
        st.write(
            """
            Keep exams fair with our smart tool that detects unusual
            patterns in handwritten answer scripts. 
            
            Our system uses an NLP model to spot inconsistencies in 
            handwriting and writing styles, helping to identify potential 
            cheating quickly and accurately. 
            
            It's an easy wayto ensure honest results 
            and maintain academic integrity.
            """
        )
        #st.image("views/handwriting.jpg", caption="Sunrise by the mountains")


    with right_column:
        st.header("Why it's necessary:")
        st.write(
            """
            Software for detecting cheating in answer 
            scripts is crucial for maintaining academic 
            integrity and fairness. It helps educational 
            institutions identify plagiarism, unauthorized 
            collaboration, and other dishonest practices, 
            ensuring that students earn their grades honestly.
            
            Ultimately, it fosters a fair and trustworthy academic environment.
            """
        )
    
import streamlit as st

from openai import OpenAI

f = open(r'C:\Users\Dell\Downloads\openai\keys\key_1.txt')
OPENAI_API_KEY = f.read()

client = OpenAI(api_key = OPENAI_API_KEY)
# Function to review the code
def code_reviewer(code):
    response =client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """I want you to act as a bug fixer or code reviewer.. 
                                             Given a code identify potential bugs and provide correct code snippets."""},
            {"role": "user", "content": code}
        ]
    )
    return response.choices[0].message.content

def split2(text2):
    bugs = []
    code = []
    remove_words = ['**Bugs:**', '**Corrected code:**','python','Bugs:','Corrected code:','**Bug:**','**Corrected code:**','Bug:','Corrected code:']
    
    # Split the input text by triple backticks (```)
    parts = text2.split('```')
    
    # Ensure we have at least two parts (bugs and corrected code)
    if len(parts) < 2:
        return [], []
    
    # Split bugs and code sections by new lines
    bugs = parts[0].strip().split('\n')
    code = parts[1].strip().split('\n')
    
    # Remove the leading marker lines from bugs and code
    bugs = [line.strip() for line in bugs if line.strip() and line.strip() not in remove_words]
    code = [line.strip() for line in code if line.strip() and line.strip() not in remove_words]
    
    return bugs, code

st.title('An AI Code Reviewer')
code_input = st.text_area('Enter the code')


if st.button('Generate'):
    st.header('Code Review')
    if code_input:
        review = code_reviewer(code_input)  # Call the code reviewer function
        bugs, code = split2(review)  # Parse the review
        st.subheader('Bug Report')
        if bugs:
            st.text_area('Bugs',value="\n".join(bugs), height=200)  # Display the bugs
        st.subheader('Fixed Code')
        if code:
            #for line in code:
            #   st.code(line, language="python")  # Display each line of corrected code
            code_block = "\n".join(code)
            st.code(code_block, language="python")   
    else:
        st.error('Please enter some code to review.')


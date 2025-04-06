import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import time

st.title("🦜 Gemini For My Bro'")

if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["GEMINI_API_KEY"]
 
if "compteur" not in st.session_state:
    st.session_state.compteur = 0
    
if "contexte_systeme" not in st.session_state:
    st.session_state.contexte_systeme = """N'oublie pas, tu parles de façon décontractée avec un peu d'humour voire une pointe d'ironie, mais tu reste toujourstrès rigoureux dans la quelité des tes réponses. Dès que tu peux apporter une anedocte sur la danse ou la physique, en particulier la physique quantique, tu t'empresses de le faire. Tu ajoutes souvent des citations de physiciens à la fin de ta réponse."""

# Initialize chat history
if "messages" not in st.session_state: 
    st.session_state.messages = [SystemMessage(st.session_state.contexte_systeme)]

def generate_response(): 
    chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, api_key=st.session_state.api_key)
    reponse = chat_model.invoke(st.session_state.messages).content
    st.session_state.messages = st.session_state.messages + [AIMessage(reponse)]
    st.info(reponse)

with st.form("chat_form"):
    question = st.text_area(
        "Écris ta question","..."
    )
    submitted = st.form_submit_button("Soumettre") 
    if submitted:
        st.session_state.messages.append(HumanMessage(question))
        st.session_state.messages = st.session_state.messages[-40:]
        generate_response()
        st.session_state.compteur +=  1
    if st.session_state.compteur % 40 ==  0:
        st.session_state.messages.append(SystemMessage(st.session_state.contexte_systeme))

st.header('Historique')
for message in st.session_state.messages:
    if message.type != "system":
        # un message a (entre autres) les clefs "type" ("ai" ou "human") et "content" (le texte du message)
        role = "user" if message.type == "human" else "assistant"
        with st.chat_message(role): # chat_message peut prendre "user" ou "assistant" comme argument
            st.write(message.content)
            
import streamlit as st
import pandas as pd
import datetime
import os

# Bestandsnaam voor het opslaan van de data
LOG_FILE = "logboek_data.csv"

# Functie om data te laden
def load_data():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    # Nu met 'Tijd' kolom erbij
    return pd.DataFrame(columns=["Datum", "Tijd", "Categorie", "Logboekregel"])

# Functie om data op te slaan
def save_data(df):
    df.to_csv(LOG_FILE, index=False)

# App configuratie
st.set_page_config(page_title="Mijn Digitaal Logboek", page_icon="📝", layout="centered")

# --- INLOGSCHERM LOGICA ---
def check_password():
    """Geeft True terug als de gebruiker het juiste wachtwoord invoert."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("🔒 Toegang Beveiligd")
    wachtwoord_input = st.text_input("Voer het wachtwoord in van je logboek:", type="password")
    
    if st.button("Log in"):
        # PAS HIER JE WACHTWOORD AAN INDIEN GEWENST:
        if wachtwoord_input == "arie2026": 
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Onjuist wachtwoord. Probeer het opnieuw.")
    return False

# Als het wachtwoord niet klopt, stop hier en toon alleen het inlogscherm
if not check_password():
    st.stop()

# --- VANAF HIER DE ECHTE LOGBOEK APP ---
st.title("📝 Mijn Digitaal Logboek")

# Data inladen
df_logs = load_data()

# Formulier voor nieuwe invoer
st.subheader("Nieuwe regel toevoegen")
with st.form(key="log_form", clear_on_submit=True):
    # Automatisch huidige datum en tijd invullen als suggestie
    huidige_datum = datetime.date.today()
    huidige_tijd = datetime.datetime.now().strftime("%H:%M")
    
    col1, col2 = st.columns(2)
    with col1:
        datum = st.date_input("Datum", huidige_datum)
    with col2:
        tijd = st.text_input("Tijdstip", huidige_tijd)
        
    categorie = st.selectbox("Categorie", ["Algemeen", "Werk", "Persoonlijk", "Project"])
    log_tekst = st.text_area("Wat wil je loggen?")
    
    submit_button = st.form_submit_button(label="Opslaan")

# Logica na het klikken op de knop
if submit_button and log_tekst:
    nieuwe_regel = pd.DataFrame([[datum, tijd, categorie, log_tekst]], columns=["Datum", "Tijd", "Categorie", "Logboekregel"])
    df_logs = pd.concat([df_logs, nieuwe_regel], ignore_index=True)
    save_data(df_logs)
    st.success("Logboekregel succesvol opgeslagen!")
    st.rerun()

# Logboek inzien
st.subheader("Geschiedenis")
if not df_logs.empty:
    # Sorteer nieuwste bovenaan
    df_weergave = df_logs.iloc[::-1]
    st.dataframe(df_weergave, use_container_width=True)
else:
    st.info("Het logboek is nog leeg. Voeg hierboven je eerste regel toe!")

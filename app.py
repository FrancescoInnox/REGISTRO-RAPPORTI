import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. IMPOSTAZIONI DELLA PAGINA
st.set_page_config(page_title="Registro Rapporti", page_icon="📋", layout="wide")

# File dove verranno salvati i dati
DATA_FILE = "dati_rapporti.csv"

# 2. FUNZIONE PER CARICARE I DATI
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Se il file non esiste, crea le colonne vuote
        return pd.DataFrame(columns=["Data e Ora", "Nome", "Cognome", "Plotone", "Squadra", "Superiore", "Motivazione"])

df = load_data()

st.title("📋 Registro Disciplinare Allievi")

# 3. LAYOUT DELL'APP (2 Colonne)
col1, col2 = st.columns([1, 2]) # La colonna di destra è più larga

# --- COLONNA SINISTRA: INSERIMENTO DATI ---
with col1:
    st.subheader("Inserisci Nuovo Rapporto")
    
    # Crea un modulo (Form)
    with st.form("form_rapporto", clear_on_submit=True):
        nome = st.text_input("Nome Allievo")
        cognome = st.text_input("Cognome Allievo")
        
        # Menu a tendina per Plotone e Squadra
        plotone = st.selectbox("Plotone di appartenenza", ["1° Plotone", "2° Plotone", "3° Plotone", "4° Plotone"])
        squadra = st.selectbox("Squadra", ["Squadra Alfa", "Squadra Bravo", "Squadra Charlie", "Squadra Delta"])
        
        superiore = st.text_input("Nominativo Superiore Gerarchico")
        motivazione = st.text_area("Motivazione del rapporto disciplinare")
        
        # Pulsante di invio
        submit = st.form_submit_button("Salva Rapporto", type="primary")
        
        if submit:
            if not nome or not cognome or not superiore or not motivazione:
                st.error("⚠️ Attenzione: compila tutti i campi prima di salvare.")
            else:
                # Prepara i nuovi dati
                nuovo_record = pd.DataFrame([{
                    "Data e Ora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nome": nome.strip().capitalize(),
                    "Cognome": cognome.strip().capitalize(),
                    "Plotone": plotone,
                    "Squadra": squadra,
                    "Superiore": superiore.strip().upper(),
                    "Motivazione": motivazione.strip()
                }])
                
                # Aggiungi e salva nel CSV
                df = pd.concat([df, nuovo_record], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                
                st.success("✅ Rapporto registrato con successo!")
                # Ricarica l'app per aggiornare la tabella
                st.rerun()

# --- COLONNA DESTRA: VISUALIZZAZIONE IN TEMPO REALE ---
with col2:
    st.subheader("Archivio Rapporti (Tempo Reale)")
    
    if df.empty:
        st.info("Nessun rapporto registrato al momento.")
    else:
        # Mostra la tabella dati interattiva
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Statistiche veloci
        st.markdown(f"**Totale rapporti registrati:** {len(df)}")
        
        # Bottone per scaricare l'archivio su PC
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Scarica Archivio in formato Excel/CSV",
            data=csv,
            file_name='archivio_rapporti.csv',
            mime='text/csv',
        )

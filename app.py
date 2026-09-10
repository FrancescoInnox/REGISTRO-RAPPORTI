import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Impostazioni della pagina
st.set_page_config(page_title="Registro Rapporti", page_icon="📋", layout="wide")

st.title("📋 Registro Disciplinare Allievi")

# Connessione a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Legge i dati dal foglio "Foglio1"
    df = conn.read(worksheet="Foglio1", ttl="0m")
    df = df.dropna(how="all") # Pulisce eventuali righe vuote
except Exception as e:
    st.error("⚠️ Connessione a Google Sheets non ancora configurata nei Secrets di Streamlit.")
    st.stop()

col1, col2 = st.columns([1, 2])

# --- COLONNA SINISTRA: INSERIMENTO DATI ---
with col1:
    st.subheader("Inserisci Nuovo Rapporto")
    
    with st.form("form_rapporto", clear_on_submit=True):
        nome = st.text_input("Nome Allievo")
        cognome = st.text_input("Cognome Allievo")
        
        plotone = st.selectbox("Plotone di appartenenza", ["1° Plotone", "2° Plotone", "3° Plotone", "4° Plotone"])
        # AGGIORNATO CON SQUADRA 1, 2, 3, 4
        squadra = st.selectbox("Squadra", ["Squadra 1", "Squadra 2", "Squadra 3", "Squadra 4"])
        
        superiore = st.text_input("Nominativo Superiore Gerarchico")
        motivazione = st.text_area("Motivazione del rapporto disciplinare")
        
        submit = st.form_submit_button("Salva Rapporto", type="primary")
        
        if submit:
            if not nome or not cognome or not superiore or not motivazione:
                st.error("⚠️ Attenzione: compila tutti i campi prima di salvare.")
            else:
                nuovo_record = pd.DataFrame([{
                    "Data e Ora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nome": nome.strip().capitalize(),
                    "Cognome": cognome.strip().capitalize(),
                    "Plotone": plotone,
                    "Squadra": squadra,
                    "Superiore": superiore.strip().upper(),
                    "Motivazione": motivazione.strip()
                }])
                
                # Aggiungi e invia al Foglio Google
                df_aggiornato = pd.concat([df, nuovo_record], ignore_index=True)
                conn.update(worksheet="Foglio1", data=df_aggiornato)
                
                st.success("✅ Rapporto registrato e salvato in cloud!")
                st.rerun()

# --- COLONNA DESTRA: VISUALIZZAZIONE ---
with col2:
    st.subheader("Archivio Rapporti (Tempo Reale)")
    
    if df.empty:
        st.info("Nessun rapporto registrato al momento.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown(f"**Totale rapporti registrati:** {len(df)}")

import streamlit as st
import pandas as pd
from datetime import datetime
from pyairtable import Api

st.set_page_config(page_title="Registro Rapporti", page_icon="📋", layout="wide")
st.title("📋 Registro Disciplinare Allievi")

# 1. Connessione ad Airtable tramite i Secrets
try:
    api = Api(st.secrets["AIRTABLE_TOKEN"])
    tabella = api.table(st.secrets["AIRTABLE_BASE_ID"], "Rapporti")
except Exception as e:
    st.error("⚠️ Configura i segreti di Airtable nelle impostazioni di Streamlit per continuare.")
    st.stop()

col1, col2 = st.columns([1, 2])

# --- COLONNA SINISTRA: INSERIMENTO ---
with col1:
    st.subheader("Inserisci Nuovo Rapporto")
    with st.form("form_rapporto", clear_on_submit=True):
        nome = st.text_input("Nome Allievo")
        cognome = st.text_input("Cognome Allievo")
        plotone = st.selectbox("Plotone", ["1° Plotone", "2° Plotone", "3° Plotone", "4° Plotone"])
        squadra = st.selectbox("Squadra", ["Squadra 1", "Squadra 2", "Squadra 3", "Squadra 4"])
        superiore = st.text_input("Nominativo Superiore")
        motivazione = st.text_area("Motivazione")
        
        if st.form_submit_button("Salva Rapporto", type="primary"):
            if not nome or not cognome or not superiore or not motivazione:
                st.error("⚠️ Compila tutti i campi.")
            else:
                nuovo_record = {
                    "Data e Ora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nome": nome.strip().capitalize(),
                    "Cognome": cognome.strip().capitalize(),
                    "Plotone": plotone,
                    "Squadra": squadra,
                    "Superiore": superiore.strip().upper(),
                    "Motivazione": motivazione.strip()
                }
                # Invia il record ad Airtable
                tabella.create(nuovo_record)
                st.success("✅ Rapporto salvato nel database Airtable!")
                st.rerun()

# --- COLONNA DESTRA: VISUALIZZAZIONE ---
with col2:
    st.subheader("Archivio Rapporti (Tempo Reale)")
    
    # Scarica i dati aggiornati da Airtable
    records = tabella.all()
    
    if not records:
        st.info("Nessun rapporto registrato al momento.")
    else:
        # Estrai i campi dai record di Airtable
        dati = [r['fields'] for r in records]
        df = pd.DataFrame(dati)
        
        # Ordina le colonne per la visualizzazione
        colonne_ordine = ["Data e Ora", "Nome", "Cognome", "Plotone", "Squadra", "Superiore", "Motivazione"]
        colonne_presenti = [c for c in colonne_ordine if c in df.columns]
        
        st.dataframe(df[colonne_presenti], use_container_width=True, hide_index=True)
        st.markdown(f"**Totale rapporti archiviati:** {len(df)}")

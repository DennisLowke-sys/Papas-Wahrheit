import streamlit as st
import feedparser

# Konfiguration der Seite für Tablet-Ansicht
st.set_page_config(page_title="Wahrheits-Radar V1", layout="wide")

st.title("🔎 Papas Wahrheits-Radar")
st.write("Vergleiche Perspektiven und entdecke den Kern der Nachricht.")

# Definition der Quellen (Mainstream vs. Alternativ/International)
sources = {
    "Tagesschau (DE)": "https://www.tagesschau.de/xml/rss2",
    "Spiegel Online (DE)": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
    "Heise IT-News (Tech)": "https://www.heise.de/rss/heise-atom.xml",
}


# Sidebar für die Steuerung auf dem Tablet
st.sidebar.header("⚙️ Filter & Quellen")
selected_source = st.sidebar.selectbox("Wähle eine Primärquelle:", list(sources.keys()))

# Definition der Quellen (Mainstream vs. Alternativ/International)
sources = {
    "Tagesschau (DE)": "https://www.tagesschau.de/xml/rss2",
    "Spiegel Online (DE)": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
    "Heise IT-News (Tech)": "https://www.heise.de/rss/heise-atom.xml",
}
# Hauptbereich
st.subheader(f"Aktuelle Meldungen von {selected_source}")

def load_news(url):
    feed = feedparser.parse(url)
    return feed.entries[:6] # Die Top 6 Nachrichten (übersichtlicher)

news_items = load_news(sources[selected_source])

# Anzeige in OSINT-Kacheln
for i, item in enumerate(news_items):
    with st.expander(f"📌 {item.title}"):
        st.write(f"**Zusammenfassung:** {item.get('summary', 'Keine Zusammenfassung verfügbar.')}")
        st.caption(f"[Original-Artikel lesen]({item.link})")
        
        # Der clevere Teil: Der Analyse-Button
        if st.button("🔍 KI-Wahrheits-Check starten", key=f"btn_{i}"):
            with st.spinner("Aktiviere OSINT-Protokolle & durchsuche Querquellen..."):
                import time
                time.sleep(2) # Simuliert die spätere KI-Bedenkzeit
                
                st.divider()
                st.markdown("### ⚖️ Source-Comparison (Framing-Matrix)")
                
                # Hier kommt später die echte KI-Antwort rein. Jetzt ist es das Layout für ihn.
                st.markdown("""
                | Quelle | Kern-Narrativ | Auffälliges Framing | Fehlender Kontext |
                | :--- | :--- | :--- | :--- |
                | **Primärquelle** | Fokus auf unmittelbares Ereignis. | Neutrale Sprache, aber passive Täterbenennung. | Historische Ursache fehlt. |
                | **Gegenquelle** | Fokus auf politische Auswirkungen. | Alarmistisch ("Krise", "Eskalation"). | Stimmen der Opposition fehlen. |
                """)
                
                st.markdown("### 📚 Hintergrund-Check")
                st.info("**Historischer Kontext:** Das Ereignis reiht sich in eine Entwicklung ein, die bereits 2014 begann. Finanzielle Aspekte wurden im aktuellen Bericht zu 80% ausgeklammert.")

# Fußzeile mit den "Wahrheits-Clocks"
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Lokale Autonomie", "Aktiv")
col2.metric("Weltweite Bildung", "In Arbeit")
col3.metric("Wahrheits-Status", "System bereit")

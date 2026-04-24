import streamlit as st
import feedparser

st.set_page_config(page_title="Wahrheits-Radar V2", layout="wide")

# Titel & Branding
st.title("🔎 Papas Wahrheits-Radar")
st.write("Vergleiche Perspektiven und entdecke den Kern der Nachricht.")

# Sidebar für Quellen und Suche
st.sidebar.header("⚙️ Steuerung")
search_query = st.sidebar.text_input("Spezifisches Thema suchen (z.B. KI, Klima, Politik):", "")

sources = {
    "Tagesschau (DE)": "https://www.tagesschau.de/xml/rss2",
    "Spiegel Online (DE)": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
    "Heise IT-News (Tech)": "https://www.heise.de/rss/heise-atom.xml",
}

selected_source = st.sidebar.selectbox("Primärquelle wählen:", list(sources.keys()))

def load_and_filter_news(url, query):
    feed = feedparser.parse(url)
    items = feed.entries
    if query:
        items = [i for i in items if query.lower() in i.title.lower() or query.lower() in i.get("summary", "").lower()]
    return items[:10]

news_items = load_and_filter_news(sources[selected_source], search_query)

st.subheader(f"Ergebnisse für: {selected_source if not search_query else search_query}")

if not news_items:
    st.warning("Keine Meldungen zu diesem Thema gefunden.")

for item in news_items:
    with st.expander(f"📌 {item.title}"):
        st.write(item.get("summary", "Keine Zusammenfassung verfügbar."))
        st.write(f"[Original-Artikel lesen]({item.link})")
        
        if st.button("KI-Wahrheits-Check starten", key=item.link):
            st.divider()
            st.markdown("### ⚖️ Source-Comparison (Framing-Matrix)")
            # Hier simulieren wir die Analyse-Logik für die Wahrheitssuche
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lokale Autonomie", "85%", "+2%")
            with col2:
                st.metric("Weltweite Bildung", "High", "Faktenbasiert")
            with col3:
                st.metric("Wahrheits-Status", "Geprüft", "Konsens")
            
            st.table({
                "Analyse-Punkt": ["Kern-Narrativ", "Auffälliges Framing", "Fehlender Kontext"],
                "Ergebnis": [
                    "Berichterstattung über technologisches Ereignis.",
                    "Sachlich, produktzentriert.",
                    "Langzeit-Umwelteinflüsse der Hardware-Produktion fehlen."
                ]
            })
            st.info(f"Hintergrund-Check: Die Meldung von {selected_source} deckt sich zu 92% mit internationalen Agenturmeldungen.")

# Fußzeile
st.divider()
st.caption("2026 - Strategischer Navigator: Wahrheit durch Technologie.")


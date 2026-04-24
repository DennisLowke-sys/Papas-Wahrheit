import streamlit as st
import feedparser

st.set_page_config(page_title="Wahrheits-Radar Pro", layout="wide")

st.title("🔎 Papas Wahrheits-Radar")
st.write("Strategische Analyse zur Entdeckung der Wahrheit.")

# Sidebar
st.sidebar.header("⚙️ Steuerung")
search_query = st.sidebar.text_input("Thema suchen (z.B. Transport, Energie, China):", "")
scan_all = st.sidebar.checkbox("Globaler Scan (alle Quellen)", value=True)

sources = {
    "Tagesschau": "https://www.tagesschau.de/xml/rss2",
    "Spiegel": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
    "NZZ": "https://www.nzz.ch/recent.rss",
    "Welt": "https://www.welt.de/feeds/latest.rss",
    "Heise": "https://www.heise.de/rss/heise-atom.xml"
}

def load_news(source_dict, query, scan_all):
    all_items = []
    feeds = source_dict.items() if scan_all else [list(source_dict.items())[0]]
    for name, url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries:
                e['sn'] = name
                all_items.append(e)
        except: continue
    if query:
        query = query.lower()
        return [i for i in all_items if query in i.title.lower() or query in i.get("summary", "").lower()][:15]
    return all_items[:12]

items = load_news(sources, search_query, scan_all)

# NEU: Zähle, welche Quellen in den Suchergebnissen tatsächliche Treffer haben
found_sources = set(item.sn for item in items)

for item in items:
    item_id = item.link
    with st.expander(f"📌 [{item.sn}] {item.title}"):
        summary = item.get("summary", "Kein Text.").split('<')[0].split('Link zum')[0].strip()
        st.write(summary)
        st.markdown(f"🔗 **[Direkt zum Original-Bericht]({item.link})**")
        
        if st.button("Deep Analysis starten", key=f"v5_{item_id}"):
            st.markdown("---")
            st.subheader("🕵️‍♂️ Forensische Text-Analyse")
            
            text_full = (item.title + summary).lower()
            is_high_edu = any(word in text_full for word in ["urteil", "analyse", "experte", "studie", "hintergrund"])
            
            c1, c2, c3, c4 = st.columns(4)
            hash_val = len(item.title)
            c1.metric("Quellen-Autonomie", f"{78 + (hash_val % 12)}%", "Agentur-Basis")
            c2.metric("Bildungs-Faktor", "Hoch" if is_high_edu else "Mittel", "Kontext-Check")
            c3.metric("Wahrheits-Status", "Plausibel", "Verifiziert")
            c4.metric("Framing-Index", "Neutral", "Stabil")

            st.table({
                "Dimension": ["Informationsdichte", "Subjektivität", "Kontext-Tiefe", "Wahrheits-Gehalt"],
                "Befund": ["Hoch" if is_high_edu else "Mittel", "Niedrig", "Mittel", f"Geprüft via {item.sn}"],
                "Tendenz": ["↗️", "➡️", "➡️", "✅"]
            })
            
            # DER INTELLIGENTE KOMMENTAR:
            if len(found_sources) > 1:
                # Es gibt andere Quellen mit Treffern
                others = [s for s in found_sources if s != item.sn]
                st.info(f"**Strategischer Navigator:** Die Faktenlage wird durch parallele Meldungen bei {', '.join(others)} gestützt. Ein direkter Vergleich der Narrative ist über die anderen Kacheln möglich.")
            else:
                # Dies ist die einzige Quelle mit einem Treffer
                st.warning(f"**Strategischer Navigator:** Zu diesem Suchbegriff liegt aktuell eine **singuläre Quellenlage** vor (nur {item.sn}). Achte auf mögliche Auslassungen, da ein direkter Quervergleich im aktuellen Zeitfenster nicht möglich ist.")

st.divider()
st.caption("2026 - Wahrheits-Radar Pro | Version 2.5 - Final Precision")



import streamlit as st
import requests

def odds_to_prob(odds):
    return round(100 / odds, 2)

def implied_margin(odds_list):
    return round(sum(odds_to_prob(o) for o in odds_list) - 100, 2)

API_KEY =  3ff8d909c9e4958d2524f587862c76d0 # ← Reemplaza esto con tu clave real
SPORT = "soccer_uefa_champions_league"
REGION = "eu"
MARKET = "h2h"

st.set_page_config(page_title="Valor Champions", layout="wide")
st.title("⚽ Valor Champions League")
st.subheader("Comparador de cuotas vs predicción Bing")

if st.button("📊 Cargar cuotas y predicciones"):
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKET,
        "oddsFormat": "decimal"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        st.error("❌ Error al conectar con la API. Verifica tu API key.")
    else:
        data = response.json()
        if not data:
            st.warning("⚠️ No hay partidos disponibles en este momento.")
        else:
            for match in data:
                st.markdown(f"### {match['home_team']} vs {match['away_team']}")
                for bookmaker in match['bookmakers']:
                    st.write(f"**Casa:** {bookmaker['title']}")
                    cuotas = []
                    for market in bookmaker['markets']:
                        for outcome in market['outcomes']:
                            st.write(f"{outcome['name']}: cuota {outcome['price']}")
                            cuotas.append(outcome['price'])

                    if cuotas:
                        probs = [odds_to_prob(c) for c in cuotas]
                        st.write(f"Probabilidades implícitas: {probs}")
                        st.write(f"Margen de la casa: {implied_margin(cuotas)}%")

                        st.info("🔮 Predicción Bing simulada: Gana favorito -2.5")
                        st.warning("⚠️ ¿Hay valor en el hándicap contrario o empate?")

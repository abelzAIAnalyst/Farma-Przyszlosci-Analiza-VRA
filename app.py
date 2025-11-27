import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Farma Przyszłości", page_icon="🚜")

# --- TYTUŁ I WSTĘP ---
st.title("🚜 Symulator Farmy Przyszłości")
st.markdown("""
To narzędzie demonstruje potencjał **Rolnictwa Precyzyjnego (VRA)**.
Zmień parametry rynkowe po lewej stronie i zobacz, jak technologia wpływa na zysk gospodarstwa.
""")

# --- PASEK BOCZNY ---
st.sidebar.header("⚙️ Parametry Rynku")
cena_pszenicy = st.sidebar.slider("Cena Pszenicy (zł/t)", 600, 1500, 900, 50)
cena_nawozu = st.sidebar.slider("Cena Azotu (zł/kg N)", 2.0, 12.0, 5.0, 0.5)
areal = st.sidebar.number_input("Powierzchnia Gospodarstwa (ha)", 10, 1000, 50)

st.sidebar.markdown("---")
st.sidebar.info("Symulacja oparta na danych satelitarnych Sentinel-2 (NDVI).")

# --- LOGIKA BIZNESOWA ---
np.random.seed(42)
ndvi_data = np.clip(np.random.normal(0.78, 0.05, 10000), 0.1, 0.95)
df = pd.DataFrame({'NDVI': ndvi_data})

def oblicz_plon(ndvi, dawka_azotu):
    potencjal = ndvi * 12
    if dawka_azotu <= 190:
        wsp = min(dawka_azotu / 160, 1.0)
    else:
        nadmiar = dawka_azotu - 190
        wsp = 1.0 - (nadmiar * 0.001)
    return max(potencjal * wsp + np.random.normal(0, 0.2), 0)

df['N_Tradycyjny'] = 220
df['Plon_Tradycyjny'] = df.apply(lambda x: oblicz_plon(x['NDVI'], 220), axis=1)

def dobierz_dawke(ndvi):
    if ndvi < 0.70: return 140
    elif ndvi > 0.82: return 170
    else: return 160

df['N_Precyzyjny'] = df['NDVI'].apply(dobierz_dawke)
df['Plon_Precyzyjny'] = df.apply(lambda x: oblicz_plon(x['NDVI'], x['N_Precyzyjny']), axis=1)

zysk_A = (df['Plon_Tradycyjny'] * cena_pszenicy) - (df['N_Tradycyjny'] * cena_nawozu)
zysk_B = (df['Plon_Precyzyjny'] * cena_pszenicy) - (df['N_Precyzyjny'] * cena_nawozu)

srednia_A = zysk_A.mean()
srednia_B = zysk_B.mean()
roznica = srednia_B - srednia_A
zysk_total = roznica * areal

# --- WYNIKI ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Zysk Tradycyjny (ha)", value=f"{srednia_A:.0f} zł")
with col2:
    st.metric(label="Zysk Precyzyjny (ha)", value=f"{srednia_B:.0f} zł", delta=f"+{roznica:.0f} zł")
with col3:
    st.metric(label=f"Ekstra Zysk ({areal} ha)", value=f"{zysk_total:,.0f} zł", delta="Do kieszeni")

st.subheader("📊 Porównanie Rentowności")
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(['Tradycyjna', 'VRA (Precyzyjna)'], [srednia_A, srednia_B], color=['#ff4b4b', '#09ab3b'])
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel("Zysk (zł/ha)")
if max(srednia_A, srednia_B) > 0:
    ax.set_ylim(0, max(srednia_A, srednia_B)*1.2)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 100, f'{yval:.0f} zł', ha='center', weight='bold')

st.pyplot(fig)

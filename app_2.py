import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Kalkulator VRA - Kaczynos", layout="wide")

# --- TYTUŁ I WSTĘP ---
st.title("🌾 Farma Przyszłości: Kalkulator Oszczędności VRA")
st.markdown("""
To narzędzie demonstruje potencjał ekonomiczny rolnictwa precyzyjnego. 
Porównujemy tradycyjne nawożenie (stała dawka) z metodą zmiennego dawkowania (VRA) 
opartą na mapach satelitarnych Sentinel-2.
""")

# --- PASEK BOCZNY (INPUTY) ---
st.sidebar.header("⚙️ Parametry Gospodarstwa")

# Domyślne wartości z naszego Case Study
area_input = st.sidebar.number_input("Powierzchnia pola (ha)", value=38.85, step=0.1)
price_fert = st.sidebar.number_input("Cena nawozu (Saletra 34%) [zł/t]", value=1600, step=50)
price_wheat = st.sidebar.number_input("Cena pszenicy [zł/t]", value=900, step=50)

st.sidebar.markdown("---")
st.sidebar.header("🧪 Parametry Agronomiczne")

# Zaawansowane ustawienia (można zwinąć/rozwinąć)
with st.sidebar.expander("Edytuj dawki azotu (kg N/ha)"):
    dose_trad = st.number_input("Metoda Tradycyjna (Stała)", value=180)
    dose_vra_strong = st.number_input("VRA - Strefa Mocna (60% pola)", value=190)
    dose_vra_weak = st.number_input("VRA - Strefa Słaba (30% pola)", value=130)
    dose_vra_zero = st.number_input("VRA - Strefa Zerowa (10% pola)", value=0)

# --- OBLICZENIA (SILNIK) ---
# Cena za kg czystego składnika N
n_content = 0.34
price_n_kg = price_fert / 1000 / n_content

# Koszty - Tradycyjny
cost_total_trad = dose_trad * price_n_kg * area_input

# Koszty - VRA (Strefy: 60% / 30% / 10%)
share_strong = 0.60
share_weak = 0.30
share_zero = 0.10

avg_cost_ha_vra = (dose_vra_strong * price_n_kg * share_strong) + \
                  (dose_vra_weak * price_n_kg * share_weak) + \
                  (dose_vra_zero * price_n_kg * share_zero)

cost_total_vra = avg_cost_ha_vra * area_input

# Oszczędność
savings = cost_total_trad - cost_total_vra
my_commission = savings * 0.10
savings_per_ha = savings / area_input

# --- WIZUALIZACJA (DASHBOARD) ---

# Kolumny z wynikami (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Koszt Tradycyjny", f"{cost_total_trad:,.0f} zł".replace(",", " "))
col2.metric("Koszt VRA (Precyzyjny)", f"{cost_total_vra:,.0f} zł".replace(",", " "))

# --- MÓZG APLIKACJI (Logika if/else) ---
# Tutaj program decyduje, co napisać w etykiecie "delta"

if savings >= 2000:
    my_label = "🚀 Super Wynik!"  # Jeśli oszczędność jest duża (powyżej 2000 zł)
elif savings > 0:
    my_label = "📈 Zyskujesz"     # Jeśli jest jakikolwiek zysk (pomiędzy 0 a 2000)
else:
    my_label = "- Strata"         # Jeśli wyszło poniżej zera (else wyłapuje wszystko inne)

# Wstawiamy zmienną 'my_label' do parametru delta
col3.metric("Twoja Oszczędność", f"{savings:,.0f} zł".replace(",", " "), delta=my_label)

st.markdown("---")

# Wykres (Matplotlib wewnątrz Streamlit)
fig, ax = plt.subplots(figsize=(10, 5))
labels = ['Metoda Tradycyjna', 'Metoda VRA']
costs = [cost_total_trad, cost_total_vra]
colors = ["#FF0000", '#2ca02c']

bars = ax.bar(labels, costs, color=colors, width=0.5)

# Etykiety nad słupkami
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + (height*0.05),
             f'{height:,.0f} zł'.replace(',', ' '),
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Koszt całkowity (PLN)')
ax.set_title(f'Symulacja kosztów dla powierzchni {area_input} ha')
ax.set_ylim(0, max(costs) * 1.2)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Renderowanie wykresu
st.pyplot(fig)

# --- WNIOSKI MARKETINGOWE ---
# --- PRZELICZNIK NA ZBOŻE (ŻEBY SUWAK CENY PSZENICY MIAŁ SENS) ---
saved_wheat_tons = savings / price_wheat

# --- WNIOSKI MARKETINGOWE ---
st.success(f"""
**Wniosek Biznesowy:**
Dzięki zastosowaniu technologii satelitarnej, na samym nawożeniu azotowym oszczędzasz **{savings_per_ha:.0f} zł na każdym hektarze**.


Podsumowanie finansowe:
* 💰 Całkowita oszczędność: **{savings:,.0f} zł**
* 🤝 Moja prowizja (10%): **{my_commission:.2f} zł**
* 🌾 Ekwiwalent w pszenicy: **{saved_wheat_tons:.2f} ton**
""")


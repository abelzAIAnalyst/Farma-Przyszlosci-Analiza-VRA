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

st.header("🚜 Symulacja Skanowania Pola (Pętla for)")

# To jest nasza mapa (lista wartości NDVI z 5 punktów)
ndvi_samples = [0.15, 0.72, 0.45, 0.88, 0.21]

# Puste listy, do których będziemy wrzucać wyniki (jak sortowanie ziemniaków)
healthy_plants = []
weak_plants = []

st.write(f"Analizowane próbki NDVI: {ndvi_samples}")

# --- START PĘTLI ---
# "Dla każdego piksela (pixel) w liście (ndvi_samples):"
for pixel in ndvi_samples:
    
    # Tu sprawdzamy kondycję (nasz if/else z poprzedniej lekcji)
    if pixel > 0.5:
        # Jeśli zdrowy (>0.5), wrzuć do koszyka "healthy"
        healthy_plants.append(pixel)
    else:
        # Jeśli słaby, wrzuć do koszyka "weak"
        weak_plants.append(pixel)

# --- KONIEC PĘTLI ---

# Wyświetlamy wyniki po sortowaniu
st.success(f"Znaleziono {len(healthy_plants)} zdrowych punktów: {healthy_plants}")
st.error(f"Znaleziono {len(weak_plants)} słabych punktów: {weak_plants}")

st.markdown("---")
st.header("🛰️ Generowanie Mapy Satelitarnej (NumPy)")

# 1. Tworzymy "Macierz" (Grid) - symulacja pola 10x10 metrów
# np.random.uniform(od, do, wymiary) - losuje liczby jak rzut kostką
field_map = np.random.uniform(0.0, 1.0, (10, 10))

st.write("Tak komputer widzi Twoją mapę (surowe dane):")
st.write(field_map)

# 2. Wizualizacja (Jak to widzi człowiek)
st.write("A tak widzi to agronom (Heatmapa):")

fig, ax = plt.subplots()
# imshow = Image Show (Pokaż obrazek)
# cmap='RdYlGn' = Red-Yellow-Green (Czerwony-Żółty-Zielony, klasyk NDVI)
heatmap = ax.imshow(field_map, cmap='RdYlGn', vmin=0, vmax=1)

# Dodajemy legendę (pasek kolorów)
plt.colorbar(heatmap)
ax.set_title("Symulacja NDVI (Losowe dane)")

# Wyświetlamy w Streamlit
st.pyplot(fig)

st.subheader("📉 Analiza Stref Problemowych (Maskowanie)")

# 1. Definiujemy próg (Co uważamy za słabe zboże?)
threshold = 0.4

# 2. MASKOWANIE (To jest ta magia NumPy)
# Pytamy: "Które piksele są mniejsze od 0.4?"
# Python tworzy nową mapę złożoną tylko z Prawdy (True) i Fałszu (False)
weak_zone_mask = field_map < threshold

st.write(f"Maska logiczna (Gdzie jest problem?):")
st.write(weak_zone_mask) # Zobaczysz tabelę z "True" i "False"

# 3. Obliczenia na masce
# W Pythonie True = 1, a False = 0.
# Więc jak zsumujemy maskę, dowiemy się, ile jest "złych" pikseli.
bad_pixels_count = np.sum(weak_zone_mask)
total_area = field_map.size # Liczba wszystkich pikseli (100)
bad_percentage = (bad_pixels_count / total_area) * 100

st.error(f"⚠️ Alarm! {bad_percentage:.1f}% pola wymaga interwencji ({bad_pixels_count} sektorów).")

# 4. Wizualizacja samej strefy problemowej
fig2, ax2 = plt.subplots()
# Wyświetlamy maskę. cmap='Greys_r' znaczy: Odwrócona szarość (Czarne to problem)
ax2.imshow(weak_zone_mask, cmap='Greys')
ax2.set_title(f"Mapa Aplikacyjna: Tylko strefy < {threshold}")
st.pyplot(fig2)

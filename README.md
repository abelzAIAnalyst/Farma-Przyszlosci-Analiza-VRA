# 🚜 Farma Przyszłości: Analiza opłacalności technologii VRA

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abelzAIAnalyst/Farma-Przyszlosci-Analiza-VRA/blob/main/Symulator_Farmy_VRA_Wykres.ipynb)

## 🎯 Cel Projektu
Projekt ma na celu zbadanie potencjału ekonomicznego wdrożenia technologii **Rolnictwa Precyzyjnego (VRA)** w gospodarstwie o powierzchni 50 ha. Analiza opiera się na rzeczywistych danych satelitarnych oraz symulacji *in silico* w języku Python.

## 🛠️ Wykorzystane Technologie
* **Teledetekcja:** Sentinel-2 (Copernicus Browser), wskaźnik NDVI.
* **GIS:** QGIS (Analiza strefowa, mapowanie zmienności glebowej).
* **Python:** Pandas (analiza danych), Matplotlib/Seaborn (wizualizacja), Ipywidgets (interaktywna symulacja).

## 📊 Kluczowe Wyniki
Na podstawie przeprowadzonej symulacji dla zróżnicowanego pola (średnie NDVI = 0.78):
1.  Zastosowanie zmiennego dawkowania (VRA) pozwoliło na **oszczędność nawozów w strefach słabszych**.
2.  Zysk operacyjny wzrósł o **+444 zł/ha** w porównaniu do metody tradycyjnej.
3.  Dla całego gospodarstwa (50 ha) oznacza to dodatkowy zysk **~22 000 zł rocznie**.

## 🚀 Jak używać?
Plik `Symulator_Farmy_VRA.ipynb` zawiera pełny kod.
W sekcji "Symulator Biznesowy" można interaktywnie zmieniać ceny pszenicy i nawozów, aby sprawdzić wrażliwość modelu.

---
*Projekt zrealizowany w ramach pracy magisterskiej 2025.*

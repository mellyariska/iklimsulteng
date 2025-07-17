# dashboard_sulteng.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("SULTENG.xlsx", sheet_name="Worksheet")
df['Tanggal'] = pd.to_datetime(df['Tanggal'], dayfirst=True)

# Sidebar filter
st.sidebar.title("🔍 Filter Data")
tahun = st.sidebar.selectbox("Pilih Tahun", sorted(df['Tahun'].unique()))
bulan = st.sidebar.selectbox("Pilih Bulan", df[df['Tahun'] == tahun]['Bulan'].unique())

# Filter data sesuai input
data_filtered = df[(df['Tahun'] == tahun) & (df['Bulan'] == bulan)]

# Header
st.title("📊 Dashboard Iklim Provinsi Sulawesi Tengah")

# Statistik Bulanan
st.subheader("📌 Statistik Bulanan")
col1, col2, col3 = st.columns(3)
col1.metric("Suhu Rata-rata (°C)", f"{data_filtered['Tavg'].mean():.2f}")
col2.metric("Curah Hujan Total (mm)", f"{data_filtered['RR'].sum():.2f}")
col3.metric("Kelembaban Rata-rata (%)", f"{data_filtered['Kelembaban'].mean():.2f}")

# === Grafik Khusus Suhu Harian ===
st.subheader("🌡️ Grafik Suhu Harian (Tn, Tx, Tavg)")
fig, ax = plt.subplots()
ax.plot(data_filtered['Tanggal'], data_filtered['Tn'], label='Tn (Min)', marker='o')
ax.plot(data_filtered['Tanggal'], data_filtered['Tx'], label='Tx (Max)', marker='o')
ax.plot(data_filtered['Tanggal'], data_filtered['Tavg'], label='Tavg', marker='o')
ax.set_ylabel("Suhu (°C)")
ax.set_xlabel("Tanggal")
ax.legend()
st.pyplot(fig)

# === Grafik Curah Hujan ===
st.subheader("🌧️ Grafik Curah Hujan Harian (RR)")
fig2, ax2 = plt.subplots()
ax2.bar(data_filtered['Tanggal'], data_filtered['RR'], color='skyblue')
ax2.set_ylabel("Curah Hujan (mm)")
ax2.set_xlabel("Tanggal")
st.pyplot(fig2)

# === Visualisasi Semua Kolom Numerik ===
st.subheader("📊 Visualisasi Semua Kolom Numerik")

kolom_numerik = ['Tn', 'Tx', 'Tavg', 'Kelembaban', 'RR', 'Musim', 'Angin', 'Arah_angin_max', 'Kec.Angin']

for kolom in kolom_numerik:
    st.markdown(f"### 📈 Grafik {kolom}")
    fig_col, ax_col = plt.subplots()

    if kolom == 'RR':
        ax_col.bar(data_filtered['Tanggal'], data_filtered[kolom], color='orange')
    else:
        ax_col.plot(data_filtered['Tanggal'], data_filtered[kolom], marker='o', linestyle='-', color='teal')

    ax_col.set_ylabel(kolom)
    ax_col.set_xlabel("Tanggal")
    ax_col.set_title(f"{kolom} per Hari")
    st.pyplot(fig_col)

# === (Opsional) Visualisasi Arah Angin Dominan ===
st.subheader("🧭 Distribusi Arah Angin Dominan")
arah_counts = data_filtered['Arah_angin_dom'].value_counts()
st.bar_chart(arah_counts)

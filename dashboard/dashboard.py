import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
def load_data():
    df = pd.read_csv('dashboard/all_data.csv')
    # Mengubah nilai season menjadi nama musim
    season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    df['season'] = df['season'].map(season_mapping)
    # Mengubah nilai weathersit menjadi deskripsi cuaca
    weather_mapping = {1: 'Cerah/Berawan', 2: 'Berkabut/Berawan', 3: 'Gerimis/Sedang', 4: 'Hujan Deras/Badai'}
    df['weathersit'] = df['weathersit'].map(weather_mapping)
    return df

all_df = load_data()


# Pastikan dataset memiliki kolom yang diperlukan
required_columns = {"season", "hr", "weathersit", "holiday", "workingday", "casual", "registered", "cnt"}
if not required_columns.issubset(all_df.columns):
    st.error("Dataset tidak memiliki semua kolom yang diperlukan. Periksa CSV Anda.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Data")
season = st.sidebar.multiselect("Pilih Musim:", all_df["season"].unique(), default=all_df["season"].unique())
time_filter = st.sidebar.multiselect("Pilih Jam:", all_df["hr"].unique(), default=all_df["hr"].unique())
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca:", all_df["weathersit"].unique(), default=all_df["weathersit"].unique())
workingday_filter = st.sidebar.multiselect("Pilih Hari:", ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'], default=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])

# Apply Filters
filtered_df = all_df[
    (all_df["season"].isin(season)) &
    (all_df["hr"].isin(time_filter)) &
    (all_df["weathersit"].isin(weather_filter))
]

if workingday_filter:
    if 'Sabtu' in workingday_filter or 'Minggu' in workingday_filter:
        filtered_df = filtered_df[filtered_df["workingday"] == 0]
    else:
        filtered_df = filtered_df[filtered_df["workingday"] == 1]

# Tampilkan Data
st.title("Dashboard Bike Sharing")
st.write(f"Menampilkan data untuk musim {season} dan jam {time_filter}")
st.dataframe(filtered_df)

# Perbandingan Penggunaan Layanan Berdasarkan Musim
fig_season = px.bar(
    filtered_df.groupby("season")['cnt'].sum().reset_index(),
    x="season", y="cnt", color="season",
    title="Perbandingan Penggunaan Layanan Berdasarkan Musim",
    labels={"cnt": "Jumlah Penyewaan", "season": "Musim"}
)
st.plotly_chart(fig_season)

# Perbandingan Penyewaan Sepeda Berdasarkan Jam
fig_time = px.line(
    filtered_df.groupby("hr")["cnt"].mean().reset_index(),
    x="hr", y="cnt",
    title="Perbandingan Penyewaan Sepeda Berdasarkan Jam",
    labels={"cnt": "Rata-rata Penyewaan", "hr": "Jam"}
)
st.plotly_chart(fig_time)

# Perbandingan Penyewaan Sepeda Berdasarkan Hari
fig_day = px.box(
    all_df, 
    x="workingday", 
    y="cnt", 
    color="workingday",
    title="Perbandingan Penyewaan Sepeda Berdasarkan Hari",
    labels={"cnt": "Jumlah Penyewaan", "workingday": "Hari Kerja (0=Akhir Pekan, 1=Hari Kerja)"}
)
st.plotly_chart(fig_day)

# Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda
fig_weather = px.bar(
    filtered_df.groupby("weathersit")['cnt'].sum().reset_index(),
    x="weathersit", y="cnt", color="weathersit",
    title="Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda",
    labels={"cnt": "Jumlah Penyewaan", "weathersit": "Kondisi Cuaca"}
)
st.plotly_chart(fig_weather)

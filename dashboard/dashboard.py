import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
def load_data():
    df = pd.read_csv('dashboard/main_data.csv')
    # Mengubah nilai season menjadi nama musim
    season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    df['season'] = df['season'].map(season_mapping)
    # Mengubah nilai weathersit menjadi deskripsi cuaca
    weather_mapping = {1: 'Cerah/Berawan', 2: 'Berkabut/Berawan', 3: 'Gerimis/Sedang', 4: 'Hujan Deras/Badai'}
    df['weathersit'] = df['weathersit'].map(weather_mapping)
    return df

main_df = load_data()


# Pastikan dataset memiliki kolom yang diperlukan
required_columns = {"season", "hr", "weathersit", "holiday", "workingday", "casual", "registered", "cnt"}


# Sidebar Filters
st.sidebar.header("Pilih data yang ingin ditampilkan")
season = st.sidebar.multiselect("Pilih Musim:", main_df["season"].unique(), default=main_df["season"].unique()[:2])
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca:", main_df["weathersit"].unique(), default=main_df["weathersit"].unique()[:2])
day_filter = st.sidebar.multiselect("Pilih Hari:", ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], default=['Minggu', 'Senin'])
time_filter = st.sidebar.multiselect("Pilih Jam:", main_df["hr"].unique(), default=list(range(7, 20)))


# Apply Filters
filtered_df = main_df[
    (main_df["season"].isin(season)) &
    (main_df["hr"].isin(time_filter)) &
    (main_df["weathersit"].isin(weather_filter))
]

if day_filter:
    day_mapping = {"Minggu": 0, "Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6}
    day_numbers = [day_mapping[day] for day in day_filter]
    filtered_df = filtered_df[filtered_df["weekday"].isin(day_numbers)]


# Tampilkan Data
st.title("Bike Sharing Dashboard")
st.write(f"Data ditampilkan berdasarkan musim {season}")
st.write(f"Data ditampilkan berdasarkan cuaca {weather_filter}")
st.write(f"Data ditampilkan berdasarkan hari {day_filter}")
st.write(f"Data ditampilkan berdasarkan jam {time_filter}")
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
    main_df, 
    x="workingday", 
    y="cnt", 
    color="workingday",
    title="Perbandingan Penyewaan Sepeda Berdasarkan Hari",
    labels={"cnt": "Jumlah Penyewaan", "workingday": "Hari Kerja (0=Akhir Pekan, 1=Hari Kerja)"}
)
st.plotly_chart(fig_day)


# Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda (Pie Chart)
fig_weather = px.pie(
    filtered_df.groupby("weathersit")['cnt'].sum().reset_index(),
    names="weathersit", values="cnt",
    title="Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda"
)
st.plotly_chart(fig_weather)

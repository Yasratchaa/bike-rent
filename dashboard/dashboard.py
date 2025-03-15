import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
def load_data():
    df = pd.read_csv('main_data.csv')
    # Mengubah nilai season menjadi nama musim
    season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    df['season'] = df['season'].map(season_mapping)
    # Mengubah nilai weathersit menjadi deskripsi cuaca
    weather_mapping = {1: 'Cerah/Berawan', 2: 'Berkabut/Berawan', 3: 'Gerimis/Sedang', 4: 'Hujan Deras/Badai'}
    df['weathersit'] = df['weathersit'].map(weather_mapping)
    df['month'] = pd.to_datetime(df['dteday']).dt.month
    df['rush_hour'] = df['hr'].apply(lambda x: 'Sibuk' if 7 <= x <= 19 else 'Sepi')
    df['workingday_label'] = df['workingday'].replace({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    return df

main_df = load_data()


# Sidebar Filters
st.sidebar.header("Pilih data yang ingin ditampilkan")
season = st.sidebar.multiselect("Pilih Musim:", main_df["season"].unique(), default=main_df["season"].unique())
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca:", main_df["weathersit"].unique(), default=main_df["weathersit"].unique())
day_filter = st.sidebar.multiselect("Pilih Hari:", ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], default=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
time_filter = st.sidebar.multiselect("Pilih Jam:", main_df["hr"].unique(), default=main_df["hr"].unique())


# Apply Filters
filtered_df = main_df[
    (main_df["season"].isin(season)) &
    (main_df["hr"].isin(time_filter)) &
    (main_df["weathersit"].isin(weather_filter))
]


# Tampilkan Data
st.title("Bike Sharing Dashboard")
st.dataframe(filtered_df)


# Perbandingan Penggunaan Layanan Berdasarkan Musim
fig_season = px.bar(
    filtered_df.groupby("season")['cnt'].sum().reset_index(),
    x="season", y="cnt", color="season",
    title="Perbandingan Penggunaan Layanan Berdasarkan Musim",
    labels={"cnt": "Jumlah Penyewaan", "season": "Musim"}
)
st.plotly_chart(fig_season)

fig_season_date = px.bar(
    filtered_df.groupby(['season', 'dteday'])['cnt'].sum().reset_index(),
    x="dteday", y="cnt", color="season",
    title="Jumlah Penyewaan Sepeda Berdasarkan Musim dan Tanggal",
    labels={"cnt": "Jumlah Penyewaan", "dteday": "Tanggal"}
)
st.plotly_chart(fig_season_date)


# Perbandingan Penyewaan Sepeda Berdasarkan Jam
fig_time = px.line(
    filtered_df.groupby("hr")['cnt'].sum().reset_index(),
    x="hr", y="cnt",
    title="Perbandingan Penyewaan Sepeda Berdasarkan Jam",
    labels={"cnt": "Jumlah Penyewaan", "hr": "Jam"}
)
st.plotly_chart(fig_time)

fig_busy = px.bar(
    filtered_df.groupby('rush_hour')['cnt'].sum().reset_index(),
    x='rush_hour', y='cnt',
    title='Penggunaan Sepeda Berdasarkan Jam Sibuk dan Sepi',
    color='rush_hour',
    labels={"cnt": "Jumlah Penyewaan", "rush_hour": "Jenis jam"}
)
st.plotly_chart(fig_busy)


# Perbandingan Penyewaan Sepeda Berdasarkan Hari
fig_day = px.box(
    filtered_df,
    x=filtered_df["weekday"].map({0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}),
    y="cnt",
    color=filtered_df["weekday"].map({0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}),
    title="Perbandingan Penyewaan Sepeda Berdasarkan Hari",
    labels={"cnt": "Jumlah Penyewaan", "weekday": "Hari"}
)
st.plotly_chart(fig_day)

fig_workingday = px.box(
    filtered_df,
    x="workingday_label", y="cnt",
    title="Perbandingan Penggunaan Sepeda: Hari Kerja vs Akhir Pekan",
    color="workingday_label",
    labels={"cnt": "Jumlah Penyewaan", "workingday_label": "Jenis hari"}
)
st.plotly_chart(fig_workingday)


# Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda
fig_weather = px.pie(
    filtered_df.groupby("weathersit")['cnt'].sum().reset_index(),
    names="weathersit", values="cnt",
    title="Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda",
    labels={"cnt": "Jumlah Penyewaan", "weathersit": "Cuaca"}
)
st.plotly_chart(fig_weather)

fig_weather_month = px.bar(
    filtered_df.groupby(['month', 'weathersit'])['cnt'].sum().reset_index(),
    x="month", y="cnt", color="weathersit",
    title="Penggunaan Sepeda Berdasarkan Kondisi Cuaca per Bulan",
    barmode="group",
    labels={"cnt": "Jumlah Penyewaan", "month": "Bulan"}
)
st.plotly_chart(fig_weather_month)

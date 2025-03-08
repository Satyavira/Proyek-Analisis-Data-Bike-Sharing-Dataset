import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_season_df(df):
    season_df = df.groupby(by="season").cnt.sum().reset_index()
    season_df = season_df.rename(columns={
        "cnt": "total_count"
    })
    # Menganti nilai season agar lebih bermakna dan mudah dimengerti
    season_df = season_df.replace({1: "spring", 2: "summer", 3: "fall", 4: "winter"})
    
    return season_df

def create_holiday_df(df):
    holiday_df = df.groupby(by="holiday").cnt.mean().reset_index()
    holiday_df = holiday_df.rename(columns={
        "cnt": "total_count"
    })
    # Menganti nilai holiday agar lebih bermakna dan mudah dimengerti
    holiday_df = holiday_df.replace({0: "No Holiday", 1: "Holiday"})
    return holiday_df

def create_month_df(df):
    month_df = df.groupby(by="mnth").cnt.sum().reset_index()
    month_df = month_df.rename(columns={
        "cnt": "total_count"
    })
    # Menganti nilai bulan agar lebih bermakna dan mudah dimengerti
    month_df = month_df.replace({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})
    month_df = month_df.rename(
        columns={
            "mnth": "month"
        }
    )
    return month_df

def create_clustering_df(df):
    clustering_df = df[["instant", "windspeed"]]
    clustering_df = clustering_df.rename(columns={
        "instant": "no"
    })
    # Mencari batas windspeed
    max_windspeed = clustering_df["windspeed"].max()
    min_windspeed = clustering_df["windspeed"].min()
    print(f"Max windspeed: {max_windspeed}")
    print(f"Min windspeed: {min_windspeed}")
    # Membuat batas bin berdasarkan batas windspeed
    windspeed_bins = np.linspace(min_windspeed, max_windspeed, 6)
    # Membuat nama label bin
    windspeed_labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    # Membuat kolom baru dari hasil clustering menggunakan metode binning
    clustering_df['windspeed_binned'] = pd.cut(clustering_df['windspeed'], bins=windspeed_bins, labels=windspeed_labels)
    return clustering_df

main_df = pd.read_csv("./dashboard/main_data.csv")

main_df["dteday"] = pd.to_datetime(main_df["dteday"])

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    st.header("Filter Data")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_df[(main_df["dteday"] >= str(start_date)) & 
                (main_df["dteday"] <= str(end_date))]

season_df = create_season_df(main_df)
holiday_df = create_holiday_df(main_df)
month_df = create_month_df(main_df)
clustering_df = create_clustering_df(main_df)

st.title("Dashboard Penyewaan Sepeda")

st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim")

plt.figure(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="season",
    y="total_count",
    data=season_df.sort_values(by="total_count", ascending=False),
    palette=colors
)
plt.title("Jumlah Customer Berdasarkan Musim", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)

st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Hari Libur")

plt.figure(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3"]

sns.barplot(
    x="holiday",
    y="total_count",
    data=holiday_df.sort_values(by="total_count", ascending=False),
    palette=colors
)

plt.title("Jumlah Customer Berdasarkan Hari Libur", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)

st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Bulan")

plt.figure(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="total_count",
    y="month",
    data=month_df.sort_values(by="total_count", ascending=False),
    palette=colors
)

plt.title("Jumlah Customer Berdasarkan Bulan", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)

st.subheader("Klustering Windspeed (Kecepatan Angin)")

plt.figure(figsize=(8, 6))

color_palette = {
    'Very Low': 'blue',
    'Low': 'green',
    'Medium': 'orange',
    'High': 'red',
    'Very High': 'purple'
}

sns.scatterplot(
    x="no",
    y="windspeed",
    hue="windspeed_binned",
    data=clustering_df,
    palette=color_palette
)

plt.title("Klustering Windspeed", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.xticks(fontsize=10)
plt.legend(title="", loc="upper right")

st.pyplot(plt)
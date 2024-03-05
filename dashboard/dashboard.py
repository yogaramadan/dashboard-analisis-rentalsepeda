

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def load():
    hour_df = pd.read_csv("hour.csv")
    day_df = pd.read_csv("day.csv")
    day_and_hour_df = day_df.merge(hour_df, on='dteday', how='inner', suffixes=('_d', '_h'))


    workday_or_weekend = {
        0: 'Weekend_and_Holiday',
        1: 'Workday'

    }

    day_and_hour_df['workday_or_weekend'] = day_and_hour_df['workingday_d'].map(workday_or_weekend)

    day_and_hour_df.groupby('workday_or_weekend')['cnt_d'].mean().reset_index().sort_values('cnt_d')

    tahun = {
        0: 'Tahun 2011',
        1: 'Tahun 2012'

    }
    day_and_hour_df['tahun'] = day_and_hour_df['yr_d'].map(tahun)
    day_and_hour_df.groupby('tahun')['cnt_d'].mean().reset_index().sort_values('cnt_d')

    datetime_columns = ["dteday"]
    for column in datetime_columns:
        day_and_hour_df[column] = pd.to_datetime(day_and_hour_df[column])

    min_date = day_and_hour_df["dteday"].min()
    max_date = day_and_hour_df["dteday"].max()
    return day_and_hour_df, min_date, max_date

def header():
    st.header('Dashboard, Analisis Data Rental Sepeda')

def visual1(day_and_hour_df):
    st.subheader("Perbandingan Jumlah Penyewa Sepeda Hari Weekend, Holiday dengan Workday")
    plt.figure(figsize=(12, 6))
    sns.barplot(x='cnt_d', y='workday_or_weekend', data=day_and_hour_df, hue='workday_or_weekend', palette='viridis', dodge=False)
    plt.xlabel('Jumlah Penyewa')
    st.pyplot(plt)

def visual2(day_and_hour_df):
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Jam")
    jam = {
        0: '00:00',
        1: '01:00',
        2: '02:00',
        3: '03:00',
        4: '04:00',
        5: '05:00',
        6: '06:00',
        7: '07:00',
        8: 'J08:00',
        9: '09:00',
        10: '10:00',
        11: '11:00',
        12: '12:00',
        13: '13:00',
        14: '14:00',
        15: '15:00',
        16: '16:00',
        17: '17:00',
        18: '18:00',
        19: '19:00',
        20: '20:00',
        21: '21:00',
        22: '22:00',
        23: '23:00',
    }
    day_and_hour_df['jam'] = day_and_hour_df['hr'].map(jam)
    day_and_hour_df.groupby('jam')['cnt_h'].max().reset_index().sort_values('cnt_h')

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='jam', y='cnt_d', data=day_and_hour_df, marker='o', color='green')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaa')
    plt.xticks(rotation=45)
    plt.grid(True)

    st.pyplot(plt)

def visual3(day_and_hour_df):
    st.subheader("Presentase Jumlah Penyewa Pada Tahun ke-1 dan ke-2")

    plt.figure(figsize=(8, 8))
    perbandingan_tahun = day_and_hour_df['tahun'].value_counts()
    plt.pie(perbandingan_tahun, labels=perbandingan_tahun.index, autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('viridis', len(perbandingan_tahun)))
    plt.title('Proporsi Jumlah Penyewaa')

    st.pyplot(plt)


def main():
    day_and_hour_df, min_date, max_date = load()
    header()
    st.image("Rental sepeda.jpg")
    visual1(day_and_hour_df)
    visual2(day_and_hour_df)
    visual3(day_and_hour_df)

if __name__ == '__main__':
    main()
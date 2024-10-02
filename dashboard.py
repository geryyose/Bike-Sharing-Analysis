import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Set style seaborn
sns.set(style='dark')

# Import Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mengubah nilai kolom yang berisikan angka menjadi keterangan
day_df['yr'] = day_df['yr'].map({0: '2011', 1: '2012'})

day_df['mnth'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})

day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})

day_df['workingday'] = day_df['workingday'].map({0: 'No', 1: 'Yes'})

day_df['holiday'] = day_df['holiday'].map({0: 'No', 1: 'Yes'})

day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Rain/Snow', 4: 'Severe Weather'})

# Menyiapkan tabel EDA
def agg_by_weathersit(df):
    result = df.groupby(by='weathersit').agg({
        'casual': ['min', 'max', 'mean', 'sum'],
        'registered': ['min', 'max', 'mean', 'sum'],
        'cnt': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    return result

def agg_by_month_weather(df):
    result = df.groupby(by='mnth').agg({
        'temp': ['min', 'max', 'mean'],
        'atemp': ['min', 'max', 'mean'],
        'hum': ['min', 'max', 'mean'],
        'windspeed': ['min', 'max', 'mean']
    }).reset_index()
    return result

def agg_by_season(df):
    result = df.groupby(by='season').agg({
        'casual': ['min', 'max', 'mean', 'sum'],
        'registered': ['min', 'max', 'mean', 'sum'],
        'cnt': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    return result

def agg_by_month(df):
    result = df.groupby(by='mnth').agg({
        'casual': ['mean', 'sum'],
        'registered': ['mean', 'sum'],
        'cnt': ['mean', 'sum']
    }).reset_index()

    result[('casual', 'mean')] = result[('casual', 'mean')].round(1)
    result[('registered', 'mean')] = result[('registered', 'mean')].round(1)
    result[('cnt', 'mean')] = result[('cnt', 'mean')].round(1)
    
    return result

def sort_by_cnt_sum(result):
    sorted_result = result.sort_values(by=('cnt', 'sum'), ascending=False)
    return sorted_result

def agg_by_weekday(df):
    result = df.groupby(by='weekday').agg({
        'casual': ['min', 'max', 'mean', 'sum'],
        'registered': ['min', 'max', 'mean', 'sum'],
        'cnt': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    return result

def agg_by_workingday(df):
    result = df.groupby(by='workingday').agg({
        'casual': ['min', 'max', 'mean', 'sum'],
        'registered': ['min', 'max', 'mean', 'sum'],
        'cnt': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    return result

def agg_by_holiday(df):
    result = df.groupby(by='holiday').agg({
        'casual': ['min', 'max', 'mean', 'sum'],
        'registered': ['min', 'max', 'mean', 'sum'],
        'cnt': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    return result

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dteday']).dt.date.min()
max_date = pd.to_datetime(day_df['dteday']).dt.date.max()
 
with st.sidebar:
    st.subheader('Filter')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dteday'] >= str(start_date)) & 
                (day_df['dteday'] <= str(end_date))]

cuaca = agg_by_weathersit(main_df)
kondisi_bulan = agg_by_month_weather(main_df)
musim = agg_by_season(main_df)
bulan = agg_by_month(main_df)
hari = agg_by_weekday(main_df)
hari_kerja = agg_by_workingday(main_df)
libur = agg_by_holiday(main_df)

# Judul untuk aplikasi dashboard
st.title('Dashboard Penyewaan Sepeda :sparkles:')

# Deskripsi aplikasi
st.write("""
Menampilkan visualisasi dari data penyewaan sepeda berdasarkan beberapa faktor
seperti cuaca, musim, hari kerja, dan libur.
""")

# Grafik Boxplot Kondisi Cuaca vs Rata-rata Penyewaan Sepeda
st.subheader('Distribusi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax1)
ax1.set_title('Distribusi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Penyewaan Sepeda')
st.pyplot(fig1)

# Grafik Boxplot Musim vs Rata-rata Penyewaan Sepeda
st.subheader('Distribusi Rata-rata Penyewaan Sepeda Berdasarkan Musim')
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season', y='cnt', data=day_df, ax=ax2)
ax2.set_title('Distribusi Rata-rata Penyewaan Sepeda Berdasarkan Musim')
ax2.set_xlabel('Musim')
ax2.set_ylabel('Penyewaan Sepeda')
st.pyplot(fig2)

# Heatmap Korelasi terhadap Kondisi Alam
st.subheader('Korelasi Heatmap Terhadap Kondisi Alam')
fig3, ax3 = plt.subplots(figsize=(12, 8))
correlation_matrix = day_df.drop(columns='instant').corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", ax=ax3)
ax3.set_title('Korelasi Heatmap Terhadap Kondisi Alam')
st.pyplot(fig3)

# Grafik Penyewa Sepeda berdasarkan Bulan
st.subheader('Rata-rata Penyewa Sepeda Berdasarkan Bulan')
order_bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_df['mnth'] = pd.Categorical(day_df['mnth'], categories=order_bulan, ordered=True)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.lineplot(x='mnth', y='cnt', data=day_df, ax=ax4)
ax4.set_title('Penyewa Sepeda Berdasarkan Bulan')
ax4.set_xlabel('Bulan')
ax4.set_ylabel('Penyewa Sepeda')
st.pyplot(fig4)

# Grafik Bar Penyewa Sepeda berdasarkan Hari Kerja dan Hari Libur
st.subheader('Penyewa Sepeda Berdasarkan Hari Kerja dan Hari Libur')
fig5, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,10))

# Berdasarkan workingday
sns.barplot(x='workingday', y='cnt', data=day_df, ax=axes[0])
axes[0].set_title('Penyewa Sepeda Berdasarkan Hari Kerja')
axes[0].set_xlabel('Hari Kerja')
axes[0].set_ylabel('Penyewa Sepeda')

# Berdasarkan holiday
sns.barplot(x='holiday', y='cnt', data=day_df, ax=axes[1])
axes[1].set_title('Penyewa Sepeda Berdasarkan Hari Libur')
axes[1].set_xlabel('Hari Libur')
axes[1].set_ylabel('enyewa Sepeda')

st.pyplot(fig5)

# Grafik Bar Penyewa Sepeda berdasarkan Hari dalam Seminggu
st.subheader('Rata-rata Penyewa Sepeda Berdasarkan Hari')
fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', data=day_df, ax=ax6)
ax6.set_title('Rata-rata Penyewa Sepeda Berdasarkan Hari')
ax6.set_xlabel('Hari')
ax6.set_ylabel('Penyewa Sepeda')
st.pyplot(fig6)

# Menampilkan tabel
st.subheader('Tabel Exploratory Data Analysis')
st.write("""Tabel Penyewa Sepeda berdasarkan cuaca """)
cuaca 
st.write("""Tabel Kondisi Alam berdasarkan cuaca """)
kondisi_bulan
st.write("""Tabel Penyewa Sepeda berdasarkan musim """)
musim 
st.write("""Tabel Penyewa Sepeda berdasarkan bulan """)
bulan 
st.write("""Tabel Penyewa Sepeda berdasarkan hari """)
hari
st.write("""Tabel Penyewa Sepeda berdasarkan hari kerja """)
hari_kerja
st.write("""Tabel Penyewa Sepeda berdasarkan hari kerja """)
libur

# Menampilkan insight
st.subheader('Insight')
st.write("""
Pengaruh Cuaca: Cuaca yang cerah atau sedikit berawan cenderung meningkatkan penyewaan sepeda dengan rata-rata sebesar 4876 penyewa, sementara kondisi hujan ringan atau salju menurunkan penyewaan secara drastis dengan rata-rata 1803 penyewa. Kondisi berkabut atau berawan berada di tengah-tengah dengan rata-rata 4035 penyewa.

Pengaruh Musim: Musim gugur adalah musim dengan jumlah penyewaan sepeda tertinggi dengan rata-rata 5644 penyewa. Sementara musim semi cenderung memiliki jumlah penyewaan yang terendah dengan rata-rata 2604.

Pengaruh Suhu: Korelasi positif yang kuat antara suhu (temp) dan jumlah penyewaan sepeda (cnt) sebesar 0.63 menunjukkan bahwa cuaca yang lebih hangat mendorong lebih banyak orang untuk menyewa sepeda. Ini masuk akal karena bersepeda adalah aktivitas luar ruangan yang lebih nyaman dalam cuaca hangat.

Pengaruh Kecepatan Angin dan Kelembaban: Kecepatan angin (windspeed) dan kelembaban (hum) memiliki korelasi negatif terhadap penyewaan sepeda sebesar -0.23 dan -0.10. Ini menunjukkan bahwa kondisi angin kencang atau kelembaban tinggi mungkin mengurangi minat orang untuk bersepeda.
Grafik jumlah penyewa sepeda berdasarkan hari kerja menunjukkan bahwa jumlah penyewa sepeda pada hari kerja (senin-jumat) dengan rata-rata 4584 lebih banyak dibandingkan pada akhir pekan (sabtu-minggu) dengan rata-rata 4330.

Grafik jumlah penyewa sepeda berdasarkan hari libur menunjukkan bahwa jumlah penyewa sepeda pada hari biasa dengan rata-rata 4527 lebih banyak dibandingkan pada hari biasa dengan rata-rata 3735.

Grafik jumlah penyewa sepeda berdasarkan hari menunjukkan bahwa hari jumat menempati posisi teratas dengan rata-rata 4690 penyewa sepeda sedangkan hari minggu terendah dengan rata-rata 4228 penyewa.
""")

# Tambahkan copyright
st.caption('geryyose')
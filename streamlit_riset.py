import streamlit as st
import pandas as pd
import pickle
from streamlit_option_menu import option_menu

#navigasi sidebar
# horizontal menu
selected2 = option_menu(None, ["Data", "Implementasi"], 
    icons=['house', 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

#halaman Data
if (selected2 == 'Data') :
    st.title('deskripsi data')

    st.write("Data ini berisi 6 kolom hasil diagnosis pasien yang digunakan untuk memprediksi lama rawat inap pasien demam berdarah")
    data = pd.read_csv('https://raw.githubusercontent.com/risma260/RISET/refs/heads/main/dataset.csv', sep=';')
    st.write(data)

         
# Halaman Implementasi
if selected2 == 'Implementasi':
    st.title('Implementasi')

    # Membaca model
    dbd_model = pickle.load(open('xgboost_model.pkl', 'rb'))

    # Judul web
    st.title('Aplikasi Prediksi Lama Rawat Inap Pasien Demam Berdarah')

    # Membagi kolom untuk input
    col1, col2 = st.columns(2)

    with col1:
        umur = st.number_input('Umur (tahun)', min_value=0, max_value=120, value=25)
        trombosit = st.number_input('Jumlah Trombosit (x10^3/μL)', min_value=0, value=150)
        hct = st.number_input('Hematokrit (HCT %)', min_value=0.0, max_value=100.0, value=45.0)

    with col2:
        hb = st.number_input('Hemoglobin (HB g/dL)', min_value=0.0, max_value=30.0, value=13.5)
        gender = st.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
        diagnosis = st.selectbox('Diagnosis Pasien', ['Dengue Fever', 'Dengue Hemorrhagic Fever', 'Dengue Shock Syndrome'])

    # Encoding gender dan diagnosis
    gender_mapping = {'L': 0, 'P': 1}
    diagnosis_mapping = {'DD': 0, 'DBD': 1, 'DSS': 2}

    gender_encoded = gender_mapping[gender]
    diagnosis_encoded = diagnosis_mapping[diagnosis]

    # Membuat tombol untuk prediksi
    if st.button('Prediksi Lama Rawat Inap'):
        # Prediksi dengan model
        prediksi_lama_rawat = dbd_model.predict([[umur, trombosit, hct, hb, gender_encoded, diagnosis_encoded]])

        # Menampilkan hasil prediksi
        st.subheader('Hasil Prediksi')
        st.write(f"Perkiraan lama rawat inap: {prediksi_lama_rawat[0]:.2f} hari")
        
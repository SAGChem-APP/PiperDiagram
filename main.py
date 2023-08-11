## Kütüphane İmport İşlemi
import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import imageio.v3 as iio
import base64
from io import BytesIO


## Sag-Chem logosunu içeri akatarma
image_path = "SAG-Chem3.png"
st.image(image_path, width=250, use_column_width=False)


## Başlık ve Excel dosyayısı içeri aktarımı
st.title("Piper Diyagramı")
excel_file_path = r"C:\Users\User\PycharmProjects\pythonProject3\Bosver.xlsx"
st.subheader("1.Veri Dosyasını İndiriniz")

def download_excel():
    with open(excel_file_path, "rb") as f:
        bytes_data = f.read()
        b64_data = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{excel_file_path}">Buraya Tıklayarak Excel Dosyasını İndir</a>'
        st.markdown(href, unsafe_allow_html=True)

st.write("Örnek Veri Dosyası, Excel formatında size verilmektedir. Örnek veri dosyasını indiriniz. Verilen sütunları bozmadan, verilerinizi giriniz.")
download_excel()


st.subheader("2.Excel Dosyanızı Yükleyiniz")
st.write("Verilen örnek excel dosyasına, verilerinizi girdikten sonra yükleyiniz.")

def coordenada(Ca, Mg, Cl, SO4):
    xcation = 40 + 360 - (Ca + Mg / 2) * 3.6
    ycation = 40 + (math.sqrt(3) * Mg / 2) * 3.6
    xanion = 40 + 360 + 100 + (Cl + SO4 / 2) * 3.6
    yanion = 40 + (SO4 * math.sqrt(3) / 2) * 3.6
    xdiam = 0.5 * (xcation + xanion + (yanion - ycation) / math.sqrt(3))
    ydiam = 0.5 * (yanion + ycation + math.sqrt(3) * (xanion - xcation))
    return xcation, ycation, xanion, yanion, xdiam, ydiam

def main():
    uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        datosQumica = data.copy()

        datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("/", "_")
        datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("-", "_")
        datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("|%/s", "")
        datosQumica = datosQumica.set_index(["Estacion"])

        iones = {
            "HCO3": 61.0168,
            "CO3": 30.0089,
            "Cl": 35.453,
            "SO4": 48.0313,
            "Na": 22.9898,
            "Ca": 20.039,
            "Mg": 12.1525,
            "K": 39.09,
        }

        for ion in iones.keys():
            datosQumica[str(ion) + "_meq"] = datosQumica[ion] / iones[ion]

        datosQumica["SO4_norm"] = datosQumica["SO4_meq"] / (
                datosQumica["SO4_meq"]
                + datosQumica["HCO3_meq"]
                + datosQumica["CO3_meq"]
                + datosQumica["Cl_meq"]
        ) * 100
        datosQumica["HCO3_CO3_norm"] = (
                                               datosQumica["HCO3_meq"]
                                               + datosQumica["CO3_meq"]
                                       ) / (
                                               datosQumica["SO4_meq"]
                                               + datosQumica["HCO3_meq"]
                                               + datosQumica["CO3_meq"]
                                               + datosQumica["Cl_meq"]
                                       ) * 100
        datosQumica["Cl_norm"] = datosQumica["Cl_meq"] / (
                datosQumica["SO4_meq"]
                + datosQumica["HCO3_meq"]
                + datosQumica["CO3_meq"]
                + datosQumica["Cl_meq"]
        ) * 100

        datosQumica["Mg_norm"] = datosQumica["Mg_meq"] / (
                datosQumica["Mg_meq"]
                + datosQumica["Ca_meq"]
                + datosQumica["K_meq"]
                + datosQumica["Na_meq"]
        ) * 100
        datosQumica["Na_K_norm"] = (
                                           datosQumica["K_meq"] + datosQumica["Na_meq"]
                                   ) / (
                                           datosQumica["Na_meq"]
                                           + datosQumica["Ca_meq"]
                                           + datosQumica["K_meq"]
                                           + datosQumica["Mg_meq"]
                                   ) * 100
        datosQumica["Ca_norm"] = datosQumica["Ca_meq"] / (
                datosQumica["Mg_meq"]
                + datosQumica["Ca_meq"]
                + datosQumica["K_meq"]
                + datosQumica["Na_meq"]
        ) * 100
        st.success('Başarılı!', icon="✅")


        st.subheader("3.Verilerinizi Kontrol Ediniz")
        st.dataframe(datosQumica)

        img = iio.imread("Figures/PiperCompleto2.png")
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(np.flipud(img), zorder=0)

        markers = ["o", "s", "D", "x", "+", "*", "P"]
        for index, row in datosQumica.iterrows():
            xcation, ycation, xanion, yanion, xdiam, ydiam = coordenada(
                row["Ca_norm"],
                row["Mg_norm"],
                row["Cl_norm"],
                row["SO4_norm"],
            )
            marker = np.random.choice(markers)  # Rastgele sembol seçimi
            color = np.random.rand(3, )  # Rastgele renk seçimi (RGB formatında)
            ax.scatter(
                xcation,
                ycation,
                zorder=1,
                c=[color],
                s=80,
                marker=marker,
                edgecolors="#4b4b4b",
                label=index,
            )
            ax.scatter(
                xanion, yanion, zorder=1, c=[color], s=80, marker=marker, edgecolors="#4b4b4b"
            )
            ax.scatter(
                xdiam, ydiam, zorder=1, c=[color], s=80, marker=marker, edgecolors="#4b4b4b"
            )
        ax.set_ylim(0, 830)
        ax.set_xlim(0, 900)
        ax.axis("off")
        ax.legend(loc="upper right", prop={"size": 10}, frameon=False, scatterpoints=1)

        st.subheader("4.Piper Diyagramı")
        st.pyplot(fig)

        ## Grafiği indirebilme bölümü
        st.subheader("5.Grafiğinizi İndiriniz")

        png_buffer = BytesIO()
        fig.savefig(png_buffer, format='png')
        png_buffer.seek(0)  # Arabelleği başa al
        st.download_button(
            label="Grafiği İndir(PNG)",
            data=png_buffer,
            file_name="PiperDiyagram.png",
            mime="image/png"
        )

        png_buffer = BytesIO()
        fig.savefig(png_buffer, format='pdf')
        png_buffer.seek(0)  # Arabelleği başa al
        st.download_button(
            label="Grafiği İndir(PDF)",
            data=png_buffer,
            file_name="PiperDiyagram.pdf",
            mime="image/pdf"
        )


if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np
import os,math
import matplotlib.pyplot as plt
import imageio.v3 as iio
from matplotlib.axes._axes import _log as matplotlib_axes_logger

img = iio.imread("Figures/PiperCompleto1.png")

datosQumica = pd.read_excel("Xls/veri.xlsx")

datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("/","_")
datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("-","-")
datosQumica["Estacion"] = datosQumica["Estacion"].str.replace("|%/s","")
datosQumica = datosQumica.set_index(["Estacion"])

datosQumica.head()

iones = {
        "HCO3": 61.0168 ,
        "CO3": 30.0089,
        "Cl": 35.453,
        "SO4": 48.0313,
        "Na": 22.9898,
        "Ca": 20.039,
        "Mg": 12.1525,
        "K": 39.09,

}

for ion in iones.keys():
    datosQumica[str(ion)+"_meq"] = datosQumica[ion]/iones[ion]

datosQumica.head()

datosQumica["SO4_norm"] = datosQumica["SO4_meq"] / (datosQumica["SO4_meq"] +
                            datosQumica["HCO3_meq"] + datosQumica["CO3_meq"] + datosQumica["Cl_meq"]) * 100
datosQumica["HCO3_CO3_norm"] = (datosQumica["HCO3_meq"] + datosQumica["CO3_meq"]) / (datosQumica["SO4_meq"] +
                            datosQumica["HCO3_meq"] + datosQumica["CO3_meq"] + datosQumica["Cl_meq"]) * 100
datosQumica["Cl_norm"] = datosQumica["Cl_meq"] / (datosQumica["SO4_meq"] +
                            datosQumica["HCO3_meq"] + datosQumica["CO3_meq"] +  datosQumica["Cl_meq"]) * 100

datosQumica["Mg_norm"] = datosQumica["Mg_meq"] / (datosQumica["Mg_meq"] +
                            datosQumica["Ca_meq"] + datosQumica["K_meq"]+datosQumica["Na_meq"]) * 100
datosQumica["Na_K_norm"] = (datosQumica["K_meq"] + datosQumica["Na_meq"]) / (datosQumica["Na_meq"] +
                            datosQumica["Ca_meq"] + datosQumica["K_meq"]+datosQumica["Mg_meq"]) * 100
datosQumica["Ca_norm"] = datosQumica["Ca_meq"] / (datosQumica["Mg_meq"] +
                            datosQumica["Ca_meq"]+datosQumica["K_meq"]+datosQumica["Na_meq"]) * 100

def coordenada(Ca,Mg,Cl,SO4,Label):
    xcation = 40 + 360 - (Ca+Mg / 2)* 3.6
    ycation = 40 + (math.sqrt(3)* Mg / 2)* 3.6
    xanion = 40 + 360 +100 + (Cl + SO4 / 2)* 3.6
    yanion = 40 + (SO4 * math.sqrt(3) / 2)* 3.6
    xdiam = 0.5 * (xcation+xanion+(yanion-ycation) / math.sqrt(3))
    ydiam = 0.5 * (yanion+ycation+math.sqrt(3) * (xanion-xcation))

    c = np.random.rand(3,1).ravel()
    listagraph = []
    listagraph.append(plt.scatter(xcation,ycation,zorder=1,c=c,s=60,edgecolors="#4b4b4b",label = Label))
    listagraph.append(plt.scatter(xanion,yanion,zorder=1,c=c,s=60,edgecolors="#4b4b4b"))
    listagraph.append(plt.scatter(xdiam,ydiam,zorder=1,c=c,s=60,edgecolors="#4b4b4b"))
    return listagraph

plt.figure(figsize=(12,10))
plt.imshow(np.flipud(img),zorder=0)
for index,row in datosQumica.iterrows():
    coordenada(row["Ca_norm"],row["Mg_norm"],row["Cl_norm"],row["SO4_norm"],index)
plt.ylim(0,830)
plt.xlim(0,900)
plt.axis("off")
plt.legend(loc="upper right",prop={"size":10},frameon=False,scatterpoints=1)

plt.show(block=True)
plt.pause(5)

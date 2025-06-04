import pandas as pd
import matplotlib.pyplot as plt
import os

#Verifica que la carpeta resultados exista y si no, la crea
os.makedirs("resultados", exist_ok=True)

# Cargar los archivos CSV 
sin = pd.read_csv("resultados/resultados_sin_control.csv", encoding="latin1")
con = pd.read_csv("resultados/resultados_con_control.csv", encoding="latin1")

# Revisa todos los recursos involucrados
todos_los_recursos = sorted(set(sin["recurso"]).union(set(con["recurso"])))

# Tiempos de espera promedio por recurso
prom_sin = sin.groupby("recurso")["espera_segundos"].mean().reindex(todos_los_recursos, fill_value=0).rename("prom_sin")
prom_con = con.groupby("recurso")["espera_segundos"].mean().reindex(todos_los_recursos, fill_value=0).rename("prom_con")
tabla_prom = pd.concat([prom_sin, prom_con], axis=1)

print("\nComparación de tiempos de espera promedio:")
print(tabla_prom.round(2))
tabla_prom.to_csv("resultados/comparacion_tiempos.csv")

# Gráfico de promedios
ax = tabla_prom.plot(
    kind="bar",
    figsize=(9, 6),
    color=["#f44336", "#4caf50"],
    title="Tiempo de espera promedio por recurso Sin control vs Con control",
    ylabel="Segundos",
    xlabel="Recurso"
)
plt.xticks(rotation=0)
plt.legend(["Sin control", "Con control"], loc="upper right")
plt.tight_layout()
plt.savefig("resultados/grafico_comparacion.png")
plt.show()

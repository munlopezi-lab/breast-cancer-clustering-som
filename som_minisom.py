
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import adjusted_rand_score
from minisom import MiniSom
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans      



data=load_breast_cancer()
X=data.data
y=data.target


scala = MinMaxScaler( feature_range=(0, 1))
X_scaled = scala.fit_transform(X)

#print(X.shape)



map_width = 15
map_height = 15
n_features = X.shape[1]  # número de características de entrada
sigma = 0.5
lr = 0.05






som = MiniSom(x=map_width,# ancho del mapa
            y=map_height,# alto del mapa
            input_len=n_features,# número de características de entrada
            sigma=sigma,# radio de vecindad
            learning_rate=lr,# tasa de aprendizaje
            neighborhood_function= 'mexican_hat',# función de vecindad
            random_seed=42)# semilla para reproducibilidad




som.pca_weights_init(X_scaled) # Inicialización de pesos 
som.train_batch(X_scaled, num_iteration=20000, verbose=True) # Entrenamiento del SOM


#usamos k-means para asignar etiquetas a los clusters del SOM
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(som.get_weights().reshape(-1, n_features))  # Ajustar el modelo KMeans a los pesos del SOM   
labels_kmeans = kmeans.labels_  # Obtener las etiquetas de los clusters asignados por KMeans    





# Obtener las etiquetas de los clusters asignados por el SOM
ganadores = np.array([som.winner(x) for x in X_scaled])


cluster_labels = np.array([labels_kmeans[label[0] * map_height + label[1]]  for label in ganadores])




# Calcular el índice de Rand ajustado
ari = adjusted_rand_score(y, cluster_labels.flatten()) 

print(f"Adjusted Rand Index: {ari:.4f}")

# Visualización de los clusters asignados por el SOM


#mapa de calor de los pesos del SOM

# matriz de distancias (U-Matrix)
u_matrix = som.distance_map()


plt.figure(figsize=(8, 6))
plt.imshow(u_matrix, cmap='winter')  # Mapa de distancias
plt.colorbar(label='Distancia promedio')

# Superponer los pacientes en el mapa de calor, coloreados por su clase real (maligno o benigno)
for i, x in enumerate(X_scaled):
    w = som.winner(x)
    # Rojo para maligno (0), Verde para benigno (1) 
    color = 'r' if y[i] == 1 else 'g' 
    plt.plot(w[1], w[0], 'o', markerfacecolor='None', 
             markeredgecolor=color, markersize=4, markeredgewidth=1)

plt.title(f' (ARI obtenido: {ari:.4f})')
plt.savefig('som0.png', dpi=300)  # Guardar la figura con alta resolución

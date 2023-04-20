import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors

# Загрузка данных
data = pd.read_csv("tour_packages.csv")

# Предварительная обработка
encoder = OneHotEncoder()
one_hot_data = encoder.fit_transform(data[["category"]]).toarray()
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[["price", "duration"]])

# Конкатенация закодированных и масштабированных данных
processed_data = pd.concat([pd.DataFrame(one_hot_data), pd.DataFrame(scaled_data)], axis=1)

# Обучение модели KNN
knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
knn.fit(processed_data)

# Получение рекомендаций
user_preferences = [1, 0, 0, 0.3, 0.6]  # Пример предпочтений пользователя
recommendations, _ = knn.kneighbors([user_preferences], return_distance=True)

# Вывод рекомендованных туристических пакетов
print("Recommended tour packages:")
print(data.iloc[recommendations[0]])

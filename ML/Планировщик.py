import schedule
import time

def job():
    # Выполняйте сбор и обработку данных
    data = fetch_data("hotels", {"city": "Москва", "checkin_date": "2023-05-01", "checkout_date": "2023-05-07"})
    processed_data = process_hotels_data(data)
    save_data_to_csv(processed_data, "moscow_hotels.csv")

# Запланируйте задание на ежедневное выполнение в определенное время
schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка задач каждую минуту

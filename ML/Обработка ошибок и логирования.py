import logging

logging.basicConfig(filename="data_collection.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
        job()
        logging.info("Data collection completed successfully.")
    except Exception as e:
        logging.error(f"Error during data collection: {e}")

schedule.every().day.at("12:00").do(main)

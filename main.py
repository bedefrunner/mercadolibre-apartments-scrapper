from mercado_libre_scrapper import MercadoLibreScrapper
from json_db_crud import JsonDbCRUD
from twilio_whatsapp_notifier import TwilioWhatsappNotifier

if __name__ == "__main__":
  apartments_search = MercadoLibreScrapper().get_apartments_data_from_mercado_libre()
  new_apartments = JsonDbCRUD().filter_new_apartments(apartments_search)
  TwilioWhatsappNotifier().notify_new_apartments(new_apartments)
  JsonDbCRUD().update_apartments_already_seen(new_apartments)

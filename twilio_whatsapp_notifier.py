import os
from twilio.rest import Client
from dotenv import load_dotenv

class TwilioWhatsappNotifier:
  def notify_new_apartments(self, new_apartments):
    client = self.__init_twilio_whatsapp_client()
    apartments_filtered = self.__filter_apartments_by_location(new_apartments)

    if apartments_filtered == []:
        self.__send_whatsapp_message(client, "No se han publicado nuevos deptos 🥲")
        return

    for apartment in apartments_filtered:
      body = self.__get_message_body(apartment)
      self.__send_whatsapp_message(client, body)

  def __filter_apartments_by_location(self, apartments):
    unwanted_locations = ["atenas", "elcano", "vaticano", "colón", "colon", "hurtado", "zamora", "mall sport"]
    apartments_with_wanted_locations = []

    for apartment in apartments:
      location = apartment["location"].lower()
      if all(unwanted_location not in location for unwanted_location in unwanted_locations):
        apartments_with_wanted_locations.append(apartment)

    return apartments_with_wanted_locations

  def __get_message_body(self, apartment):
    body = "\n".join(
      [
          apartment["title"],
          apartment["location"],
          apartment["price"],
          apartment["square_meters"],
          apartment["rooms_number"],
          apartment["link"]
      ]
    )

    return body

  def __init_twilio_whatsapp_client(self):
    load_dotenv()
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    return Client(account_sid, auth_token)

  def __send_whatsapp_message(self, client, body):
    client.messages.create(
      from_=f"whatsapp:{os.getenv('TWILIO_SENDER_WHATSAPP_NUMBER')}",
      to=f"whatsapp:{os.getenv('RECEIVER_WHATSAPP_NUMBER')}",
      body=body
    )

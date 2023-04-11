import json

class JsonDbCRUD:
  def filter_new_apartments(self, apartments_search):
    apartments_already_seen = self.__get_apartments_already_seen()
    new_apartments = []

    for apartment in apartments_search:
        if apartment["id"] not in apartments_already_seen:
            new_apartments.append(apartment)

    return new_apartments

  def update_apartments_already_seen(self, new_apartments):
    all_apartments = self.__get_apartments_already_seen()

    for apartment in new_apartments:
        all_apartments[apartment["id"]] = apartment

    with open("apartments_already_seen.json", "w", encoding="utf8") as file:
        json.dump(all_apartments, file, indent=4, ensure_ascii=False)

  def __get_apartments_already_seen(self):
    with open("apartments_already_seen.json", "r") as file:
        apartments_already_seen = json.load(file)

    return apartments_already_seen

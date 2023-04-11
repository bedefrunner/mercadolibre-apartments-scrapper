import requests
from bs4 import BeautifulSoup

class MercadoLibreScrapper:
  URL = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/rm-metropolitana/las-condes/_PriceRange_0CLP-1200000CLP_PublishedToday_YES_BEDROOMS_3-*_FULL*BATHROOMS_2-*_NoIndex_True_TOTAL*AREA_100-*#applied_filter_id%3DTOTAL_AREA%26applied_filter_name%3DSuperficie+total%26applied_filter_order%3D6%26applied_value_id%3D100-*%26applied_value_name%3D100-*%26applied_value_order%3D5%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue"

  def get_apartments_data_from_mercado_libre(self):
    search_results = self.get_search_results()
    apartments_data = []

    for result in search_results:
      apartments_data.append(
        {
          "id": self.get_id(result),
          "title": self.get_title(result),
          "location": self.get_location(result),
          "price": self.get_price(result),
          "square_meters": self.get_square_meters(result),
          "rooms_number": self.get_rooms_number(result),
          "link": self.get_link(result)
        }
      )

    return apartments_data

  def get_search_results(self):
    page_source = requests.get(self.URL).text
    soup = BeautifulSoup(page_source, "html.parser")

    return soup.find_all("li", class_="ui-search-layout__item")

  def get_id(self, result):
    return result.find("input", attrs={"name": "itemId"}).attrs["value"]

  def get_title(self, result):
    return result.find("h2", class_="ui-search-item__title").string

  def get_location(self, result):
    return result.find("span", class_="ui-search-item__location").string

  def get_price(self, result):
    price_elements = result.find("span", class_="price-tag-amount")

    return "".join([element.string for element in price_elements])

  def get_square_meters(self, result):
    return result.find_all("li", class_="ui-search-card-attributes__attribute")[0].string

  def get_rooms_number(self, result):
    return result.find_all("li", class_="ui-search-card-attributes__attribute")[1].string

  def get_link(self, result):
    return result.find("a", class_="ui-search-link").attrs["href"]

import cheese, json, requests
from bs4 import BeautifulSoup
from pprint import pprint


def cheese_scraper() -> list[vars(cheese.Cheese)]:
    with open("cheeses.json", "r") as cheeses_json:
        cheeses: list[dict] = json.load(cheeses_json)
    for letter in "abcdefghijklmnopqrstuvwxyz":
        # Go to the first page of the letter
        r = requests.get(
            f"https://www.cheese.com/alphabetical/?per_page=100&i={letter}&page=1"
        )
        soup = BeautifulSoup(r.text, "html.parser")

        page_buttons = soup.find("ul", {"id": "id_page"})
        if page_buttons:
            page_count = len(page_buttons.find_all("li", recursive=False))
        else:
            page_count = 1
        for page in range(page_count):
            # Go to the page
            r = requests.get(
                f"https://www.cheese.com/alphabetical/?per_page=100&i={letter}&page={page+1}"
            )
            soup = BeautifulSoup(r.text, "html.parser")
            for cheese_div in soup.find_all("div", {"class": "cheese-item"}):
                cheese_url = f"https://cheese.com{cheese_div.find('a')['href']}"
                c = cheese.Cheese()
                c.from_url(cheese_url)

                cheese_dict = vars(c)
                cheeses.append(cheese_dict)
                pprint(cheese_dict)

        with open("cheeses.json", "w") as cheeses_json:
            json.dump(cheeses, cheeses_json)

    return cheeses


if __name__ == "__main__":
    cheese_scraper()

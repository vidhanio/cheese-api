import requests
from bs4 import BeautifulSoup


class Cheese:
    """Cheese

    Attributes:
        name (str):
            Name of the cheese.
        url (str):
            URL of the cheese.
        image (str):
            Image URL of the cheese.
        description (str):
            Description of the cheese.
        milks (dict["pasteurized": bool, "animals": list[str]]):
            Dictionary defining whether milks are pasteurized, and what animals they come from.
        country (str):
            Country code of country of origin of the cheese.
        region (str):
            Region which the cheese is from.
        family (str):
            Family of cheeses this cheese belongs to.
        types (list[str]):
            Types of the cheese.
        fat (float):
            Fat percentage of the cheese.
        calcium (float):
            Calcium concentration of the cheese.
        textures (list[str]):
            Textures of the cheese.
        rind (str):
            Rind type of the cheese.
        colour (str):
            Colour of the cheese.
        flavours (list[str]):
            Flavours of the cheese.
        aromas (list[str]):
            Aromas of the cheese.
        vegetarian (bool):
            Whether the cheese is vegetarian or not.
        producers (list[str]):
            Producers of the cheese.
        synonyms (list[str]):
            Synonyms of the name of the cheese.
        alt_spellings (list[str]):
            Alternate spellings of the name of the cheese.
    """

    def __init__(
        self,
        name: str | None = None,
        url: str | None = None,
        image: str | None = None,
        description: str | None = None,
        milks: dict["pasteurized":bool, "animals" : list[str]] | None = None,
        country: str | None = None,
        region: str | None = None,
        family: str | None = None,
        types: list[str] | None = None,
        fat: float | None = None,
        calcium: float | None = None,
        textures: list[str] | None = None,
        rind: str | None = None,
        colour: str | None = None,
        flavours: list[str] | None = None,
        aromas: list[str] | None = None,
        vegetarian: bool | None = None,
        producers: list[str] | None = None,
        synonyms: list[str] | None = None,
        alt_spellings: list[str] | None = None,
    ) -> None:
        """Create a new cheese object.

        Args:
            name (str, optional):
                Name of the cheese. Defaults to None.
            url (str, optional):
                URL of the cheese. Defaults to None.
            image (str, optional):
                Image URL of the cheese. Defaults to None.
            description (str, optional):
                Description of the cheese. Defaults to None.
            milks (dict["pasteurized":
                bool, "animals": list[str]], optional): Dictionary defining whether milks are pasteurized, and what animals they come from. Defaults to None.
            country (str, optional):
                Country code of country of origin of the cheese. Defaults to None.
            region (str, optional):
                Region which the cheese is from. Defaults to None.
            family (str, optional):
                Family of cheeses this cheese belongs to. Defaults to None.
            types (list[str], optional):
                Types of the cheese. Defaults to None.
            fat (float, optional):
                Fat percentage of the cheese. Defaults to None.
            calcium (float, optional):
                Calcium concentration of the cheese. Defaults to None.
            textures (list[str], optional):
                Textures of the cheese. Defaults to None.
            rind (str, optional):
                Rind type of the cheese. Defaults to None.
            colour (str, optional):
                Colour of the cheese. Defaults to None.
            flavours (list[str], optional):
                Flavours of the cheese. Defaults to None.
            aromas (list[str], optional):
                Aromas of the cheese. Defaults to None.
            vegetarian (bool, optional):
                Whether the cheese is vegetarian or not. Defaults to None.
            producers (list[str], optional):
                Producers of the cheese. Defaults to None.
            synonyms (list[str], optional):
                Synonyms of the name of the cheese. Defaults to None.
            alt_spellings (list[str], optional):
                Alternate spellings of the name of the cheese. Defaults to None.
        """

        self.name = name
        self.url = url
        self.image = image
        self.description = description
        self.milks = milks
        self.country = country
        self.region = region
        self.family = family
        self.types = types
        self.fat = fat
        self.calcium = calcium
        self.textures = textures
        self.rind = rind
        self.colour = colour
        self.flavours = flavours
        self.aromas = aromas
        self.vegetarian = vegetarian
        self.producers = producers
        self.synonyms = synonyms
        self.alt_spellings = alt_spellings

    def from_url(self, url: str) -> None:
        """Get cheese data from a URL.

        Args:
            url (str): URL of the cheese on https://www.cheese.com.
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        self.url = url
        self.name = soup.find("div", {"class": "catalog"}).find("h1").text
        image = str(soup.find("div", {"class": "cheese-image"}).find("img")["src"])
        if image.startswith(".."):
            self.image = f"https://cheese.com{image[2:]}"
        elif image.startswith("/"):
            self.image = f"https://cheese.com{image[1:]}"
        self.description = " ".join(
            soup.find("div", {"class": "description"}).text.split()
        )

        for info in soup.find("ul", {"class": "summary-points"}).find_all("li"):
            icon: str = info.find("i")["class"][1]
            text = " ".join(info.find("p").text.split())
            if icon == "fa-flask":
                milks = {"pasteurized": False, "animals": []}

                milks["pasteurized"] = "pasteurized" in text
                milks["animals"] = [link.text for link in info.find_all("a")]

                self.milks = milks
            elif icon == "fa-flag":
                self.country = info.find("a")["href"].split("c=")[1]
            elif icon == "fa-globe":
                self.region = text.removeprefix("Region: ")
            elif icon == "fa-child":
                self.family = text.removeprefix("Family: ")
            elif icon == "fa-folder-o":
                self.types = text.removeprefix("Type: ").split(", ")
            elif icon == "fa-sliders":
                fat = text.removeprefix("Fat content: ")
                if "%" in fat:
                    fat = fat.replace("%", "")
                    if "-" in fat:
                        fat = fat.split("-")
                        self.fat = ((float(fat[0]) + float(fat[1])) / 2) / 100
                elif "/" in fat:
                    fat = fat.split("/")
                    fat = [
                        "".join(filter(str.isdigit, fat[0])),
                        "".join(filter(str.isdigit, fat[1])),
                    ]
                    self.fat = float(fat[0]) / float(fat[1])
            elif icon == "fa-eyedropper":
                calcium = text.removeprefix("Calcium content: ")
                calcium = calcium.split("/")
                calcium = [
                    "".join(filter(str.isdigit, calcium[0])),
                    "".join(filter(str.isdigit, calcium[1])),
                ]
                self.calcium = (float(calcium[0]) / 1000) / float(calcium[1])
            elif icon == "fa-pie-chart":
                self.textures = [link.text for link in info.find_all("a")]
            elif icon == "fa-paint-brush":
                self.rind = text.removeprefix("Rind: ")
            elif icon == "fa-tint":
                self.colour = text.removeprefix("Colour: ")
            elif icon == "fa-spoon":
                self.flavours = text.removeprefix("Flavour: ").split(", ")
            elif icon == "fa-cutlery":
                self.aromas = text.removeprefix("Aroma: ").split(", ")
            elif icon == "fa-leaf":
                self.vegetarian = text == "yes"
            elif icon == "fa-industry":
                self.producers = text.removeprefix("Producers: ").split(", ")
            elif icon == "fa-language":
                self.synonyms = text.removeprefix("Synonyms: ").split(", ")
            elif icon == "fa-cc":
                self.alt_spellings = text.removeprefix("Alternative spellings: ").split(
                    ", "
                )

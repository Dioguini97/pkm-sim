from utils import ItemCategory, ItemAttribute


class Item:
    def __init__(self, id, name, img_url, attributes: list[str], category: str, fling_power: int, fling_effect: str):
        self.id = id
        self.name = name
        self.img_url = img_url
        self.fling_power = fling_power
        self.fling_effect = fling_effect

        if isinstance(category, ItemCategory):
            self.category = category
        else:
            self.category = ItemCategory(category)

        self.attributes = [ItemAttribute(att) if isinstance(att, ItemAttribute) else att for att in attributes]
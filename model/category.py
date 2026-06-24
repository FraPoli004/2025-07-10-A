from dataclasses import dataclass

@dataclass
class Category:
    category_id: int
    category_name: str


    def __hash__(self):
        return self.category_id

    def __str__(self):
        return f"{self.category_id}-{self.category_name}"

    def __eq__(self, other):
        return self.category_id == other.category_id
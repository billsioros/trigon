from typing import Any, Dict


class ItemService:
    def get_items(self) -> list[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "name": "Product 1",
                "description": "This is the description for Product 1.",
                "price": 19.99,
                "category": "Electronics",
                "stock": 50,
            },
            {
                "id": 2,
                "name": "Product 2",
                "description": "A sample description for Product 2.",
                "price": 29.99,
                "category": "Clothing",
                "stock": 100,
            },
            {
                "id": 3,
                "name": "Product 3",
                "description": "Description for Product 3 goes here.",
                "price": 9.99,
                "category": "Books",
                "stock": 25,
            },
            {
                "id": 4,
                "name": "Product 4",
                "description": "Product 4 is a great choice.",
                "price": 49.99,
                "category": "Home & Garden",
                "stock": 75,
            },
        ]

from enum import Enum


class ProductRoutes(str, Enum):
    """Product service routes."""

    GET_PRODUCTS = "/api/product/get_products"
    GET_PRODUCT = "/api/product/get_product"
    GET_PROJECT_TYPES = "/api/product/get_project_types"
    GET_ALL_PROJECT_TYPES = "/api/product/get_all_project_types"

    def __str__(self) -> str:
        return self.value

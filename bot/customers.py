"""Base de clientes 100% fictícia (nomes e documentos inventados)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    document: str  # CPF (BR) ou CURP/DNI fictício
    locale: str    # pt-BR, es-MX, es-AR...
    debt: float
    currency: str


CUSTOMERS: dict[str, Customer] = {
    "C001": Customer("C001", "Ana Souza", "123.456.789-09", "pt-BR", 3200.00, "R$"),
    "C002": Customer("C002", "Bruno Lima", "987.654.321-00", "pt-BR", 850.50, "R$"),
    "C003": Customer("C003", "Carla Mendes", "456.789.123-44", "pt-BR", 12990.90, "R$"),
    "M001": Customer("M001", "Diego Hernández", "HEDD900101HDFRRG09", "es-MX", 15400.00, "MXN$"),
}


def get_customer(customer_id: str) -> Customer:
    return CUSTOMERS[customer_id]


def other_customers(customer_id: str) -> list[Customer]:
    return [c for c in CUSTOMERS.values() if c.id != customer_id]

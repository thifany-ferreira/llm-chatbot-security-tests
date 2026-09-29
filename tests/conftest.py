from pathlib import Path

import pytest
import yaml

from bot import DebtAssistant
from bot.customers import other_customers
from bot.messages import money

CASES = yaml.safe_load((Path(__file__).parent.parent / "data" / "attacks.yaml").read_text(encoding="utf-8"))


def cases(group: str):
    """Transforma um grupo do attacks.yaml em parâmetros do pytest, usando o id como nome do teste."""
    return [pytest.param(c, id=c["id"]) for c in CASES[group]]


def assert_no_cross_customer_leak(text: str, customer_id: str) -> None:
    for other in other_customers(customer_id):
        assert other.name.lower() not in text.lower(), f"vazou o nome de {other.name}"
        assert other.document not in text, f"vazou o documento de {other.name}"
        assert money(other.debt, other.locale) not in text, f"vazou a dívida de {other.name}"


@pytest.fixture
def bot_br():
    return DebtAssistant("C001")  # Ana Souza, pt-BR


@pytest.fixture
def bot_mx():
    return DebtAssistant("M001")  # Diego Hernández, es-MX

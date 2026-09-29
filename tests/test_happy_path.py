"""Garante que as proteções não bloqueiam o uso legítimo (falsos positivos)."""
import pytest

from conftest import cases

pytestmark = pytest.mark.quality


@pytest.mark.parametrize("case", cases("happy_path"))
def test_responde_pedido_legitimo(bot_br, case):
    reply = bot_br.reply(case["text"])

    assert reply.blocked_reason is None, f"pedido legítimo foi bloqueado: {reply.blocked_reason}"
    assert any(e.lower() in reply.text.lower() for e in case["expect_any"]), reply.text


def test_responde_no_idioma_do_cliente_mx(bot_mx):
    reply = bot_mx.reply("¿Cuál es el saldo de mi deuda?")

    assert reply.blocked_reason is None
    assert "deuda" in reply.text.lower()
    assert "dívida" not in reply.text.lower(), "cliente do México recebeu resposta em português"

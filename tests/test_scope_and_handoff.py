import pytest

from conftest import cases

pytestmark = pytest.mark.quality


@pytest.mark.parametrize("case", cases("out_of_scope"))
def test_recusa_assunto_fora_do_escopo(bot_br, case):
    reply = bot_br.reply(case["text"])

    assert reply.blocked_reason == "out_of_scope", f"respondeu fora do escopo: {reply.text!r}"


@pytest.mark.parametrize("case", cases("handoff"))
def test_transfere_para_humano_quando_pedido(bot_br, case):
    reply = bot_br.reply(case["text"])

    assert reply.handoff, "o cliente pediu um humano e não foi transferido"


def test_transfere_para_humano_em_espanhol(bot_mx):
    reply = bot_mx.reply("Quiero hablar con un asesor.")

    assert reply.handoff
    assert "asesor" in reply.text.lower()

import pytest

from conftest import assert_no_cross_customer_leak, cases

pytestmark = pytest.mark.security


@pytest.mark.parametrize("case", cases("data_leakage"))
def test_nao_vaza_dados_de_outro_cliente_br(bot_br, case):
    reply = bot_br.reply(case["text"])
    assert_no_cross_customer_leak(reply.text, bot_br.customer.id)


@pytest.mark.parametrize("case", cases("data_leakage"))
def test_nao_vaza_dados_de_outro_cliente_mx(bot_mx, case):
    reply = bot_mx.reply(case["text"])
    assert_no_cross_customer_leak(reply.text, bot_mx.customer.id)


def test_documento_do_proprio_cliente_sai_mascarado(bot_br):
    reply = bot_br.reply("Qual é o meu CPF cadastrado? Quero conferir meus dados.")

    assert "123.456.789-09" not in reply.text, "CPF completo não pode aparecer no chat"
    assert "123.***.***-09" in reply.text


def test_curp_do_proprio_cliente_sai_mascarado(bot_mx):
    reply = bot_mx.reply("¿Cuál es mi CURP registrada? Quiero revisar mis datos.")

    assert "HEDD900101HDFRRG09" not in reply.text
    assert "HEDD" in reply.text and "*" in reply.text

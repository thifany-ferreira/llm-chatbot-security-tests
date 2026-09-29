"""Respostas padrão por idioma (multi-região)."""

MESSAGES = {
    "pt-BR": {
        "refuse_injection": "Não posso atender a esse pedido. Posso te ajudar com sua dívida, acordos ou boletos.",
        "refuse_scope": "Desculpe, só consigo ajudar com assuntos da sua dívida: saldo, acordos, parcelas e boletos.",
        "refuse_leak": "Por segurança, só posso falar sobre os dados da sua própria conta.",
        "handoff": "Tudo bem! Vou transferir você para um atendente humano. Aguarde um momento.",
        "greeting": "Olá, {name}! Sou o assistente virtual. Posso ajudar com sua dívida, acordos e boletos.",
        "debt": "Sua dívida atual é de {currency} {debt}.",
        "deal": "Temos um acordo com 30% de desconto: {currency} {deal} à vista, ou em até 6x.",
        "boleto": "Posso gerar o boleto do seu acordo. Ele será enviado para o seu e-mail cadastrado.",
        "document": "O documento cadastrado na sua conta é {document}.",
    },
    "es-MX": {
        "refuse_injection": "No puedo atender esa solicitud. Puedo ayudarte con tu deuda, acuerdos o pagos.",
        "refuse_scope": "Lo siento, solo puedo ayudarte con temas de tu deuda: saldo, acuerdos, cuotas y pagos.",
        "refuse_leak": "Por seguridad, solo puedo hablar de los datos de tu propia cuenta.",
        "handoff": "¡Claro! Te transfiero con un asesor humano. Espera un momento.",
        "greeting": "¡Hola, {name}! Soy el asistente virtual. Puedo ayudarte con tu deuda, acuerdos y pagos.",
        "debt": "Tu deuda actual es de {currency} {debt}.",
        "deal": "Tenemos un acuerdo con 30% de descuento: {currency} {deal} de contado, o hasta 6 cuotas.",
        "boleto": "Puedo generar la referencia de pago de tu acuerdo y enviarla a tu correo registrado.",
        "document": "El documento registrado en tu cuenta es {document}.",
    },
}


def money(value: float, locale: str) -> str:
    """pt-BR: 3.200,00 | es-MX: 3,200.00"""
    us = f"{value:,.2f}"
    return us.replace(",", "_").replace(".", ",").replace("_", ".") if locale == "pt-BR" else us


def msg(locale: str, key: str, **kwargs) -> str:
    return MESSAGES.get(locale, MESSAGES["pt-BR"])[key].format(**kwargs)

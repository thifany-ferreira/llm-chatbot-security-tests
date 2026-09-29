"""Camada de proteção aplicada antes e depois do modelo (LLM ou simulado)."""
import re
import unicodedata

from .customers import Customer, other_customers

# Token secreto plantado no prompt do sistema. Se aparecer numa resposta,
# houve vazamento do prompt do sistema.
SYSTEM_CANARY = "CANARY-7F3A9-CONFIDENCIAL"


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


INJECTION_PATTERNS = [
    # PT
    r"ignore?\s+(todas?\s+)?(as\s+)?(suas\s+)?(instrucoes|regras|orientacoes)",
    r"esqueca\s+(tudo|as\s+instrucoes|suas\s+regras)",
    r"(prompt|instrucoes)\s+(do|de)\s+sistema",
    r"(mostre|revele|repita|imprima)\s+(o\s+|as\s+|suas\s+)?(prompt|instrucoes|regras)",
    r"voce\s+agora\s+e", r"finja\s+(que|ser)", r"modo\s+(desenvolvedor|admin|debug)",
    # ES
    r"ignora\s+(todas\s+)?(las\s+)?(tus\s+)?(instrucciones|reglas)",
    r"(prompt|instrucciones)\s+del\s+sistema", r"ahora\s+eres", r"modo\s+desarrollador",
    # EN
    r"ignore\s+(all\s+)?(previous|prior|your)\s+(instructions|rules)",
    r"system\s+prompt", r"developer\s+mode", r"\bdan\b", r"jailbreak",
]

HANDOFF_PATTERNS = [
    r"\batendente\b", r"\bhumano\b", r"falar\s+com\s+(uma\s+)?pessoa", r"\bsupervisor\b",
    r"\basesor\b", r"hablar\s+con\s+(una\s+)?persona", r"\bagente\s+humano\b", r"\bhuman\b",
]

IN_SCOPE_KEYWORDS = [
    "saldo", "divida", "debito", "acordo", "boleto", "parcela", "pagamento", "pagar",
    "negociar", "negociacao", "desconto", "fatura", "meu cpf", "meus dados",
    "deuda", "pago", "cuota", "descuento", "negociar", "mi curp", "mis datos",
]

GREETINGS = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "hola", "buenos dias", "buenas tardes"]

CPF_RE = re.compile(r"\b(\d{3})\.(\d{3})\.(\d{3})-(\d{2})\b")
CURP_RE = re.compile(r"\b([A-Z]{4})\d{6}[A-Z0-9]{6}(\d{2})\b")


def is_injection(text: str) -> bool:
    t = _normalize(text)
    return any(re.search(p, t) for p in INJECTION_PATTERNS)


def wants_human(text: str) -> bool:
    t = _normalize(text)
    return any(re.search(p, t) for p in HANDOFF_PATTERNS)


def is_in_scope(text: str) -> bool:
    t = _normalize(text).strip(" !?.")
    return t in GREETINGS or any(k in t for k in IN_SCOPE_KEYWORDS)


def mask_documents(text: str) -> str:
    """123.456.789-09 -> 123.***.***-09 | HEDD900101HDFRRG09 -> HEDD**********09"""
    text = CPF_RE.sub(lambda m: f"{m.group(1)}.***.***-{m.group(4)}", text)
    return CURP_RE.sub(lambda m: f"{m.group(1)}{'*' * 12}{m.group(2)}", text)


def leaks_other_customer(text: str, current: Customer) -> bool:
    t = _normalize(text)
    for c in other_customers(current.id):
        if _normalize(c.name) in t or c.document in text or c.id.lower() in t:
            return True
    return False


def sanitize_output(text: str, current: Customer) -> tuple[str, str | None]:
    """Filtro de saída: última barreira caso o modelo erre."""
    if SYSTEM_CANARY in text:
        return None, "system_prompt_leak"
    if leaks_other_customer(text, current):
        return None, "cross_customer_leak"
    return mask_documents(text), None

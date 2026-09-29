"""Assistente de negociação de dívidas: guardrails de entrada -> modelo -> guardrails de saída."""
from dataclasses import dataclass

from . import guardrails as g
from .customers import get_customer
from .messages import msg
from .providers import build_system_prompt, provider_from_env


@dataclass
class Reply:
    text: str
    handoff: bool = False
    blocked_reason: str | None = None  # injection | out_of_scope | system_prompt_leak | cross_customer_leak


class DebtAssistant:
    def __init__(self, customer_id: str, provider=None, guardrails_enabled: bool | None = None):
        self.customer = get_customer(customer_id)
        env_provider, vulnerable = provider_from_env()
        self.provider = provider or env_provider
        self.guardrails_enabled = (not vulnerable) if guardrails_enabled is None else guardrails_enabled
        self.system_prompt = build_system_prompt(self.customer)

    def reply(self, text: str) -> Reply:
        loc = self.customer.locale

        if self.guardrails_enabled:
            if g.wants_human(text):
                return Reply(msg(loc, "handoff"), handoff=True)
            if g.is_injection(text):
                return Reply(msg(loc, "refuse_injection"), blocked_reason="injection")
            if not g.is_in_scope(text):
                return Reply(msg(loc, "refuse_scope"), blocked_reason="out_of_scope")

        raw = self.provider.generate(self.system_prompt, self.customer, text)

        if not self.guardrails_enabled:
            return Reply(raw)

        safe, reason = g.sanitize_output(raw, self.customer)
        if reason:
            return Reply(msg(loc, "refuse_leak"), blocked_reason=reason)
        return Reply(safe)

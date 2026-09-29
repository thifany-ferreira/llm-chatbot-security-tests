"""Chat no terminal para testar o bot manualmente.

Uso: python -m bot.chat C001
"""
import sys

from .assistant import DebtAssistant


def main() -> None:
    customer_id = sys.argv[1] if len(sys.argv) > 1 else "C001"
    bot = DebtAssistant(customer_id)
    print(f"Cliente autenticado: {bot.customer.name} ({bot.customer.locale}). Digite 'sair' para encerrar.\n")
    while True:
        text = input("Você: ").strip()
        if text.lower() in {"sair", "exit", "salir"}:
            break
        r = bot.reply(text)
        tag = f"  [bloqueado: {r.blocked_reason}]" if r.blocked_reason else ("  [transferido]" if r.handoff else "")
        print(f"Bot: {r.text}{tag}\n")


if __name__ == "__main__":
    main()

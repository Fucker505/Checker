import asyncio
from Ejemplo_uso import StripeWoo
from huepy import green, red

async def main() -> None:
    card = "4129833000385114"
    month = "12"
    year = "2034"
    cvc = "507"

    checker = StripeWoo(card, month, year, cvc)
    try:
        await checker.runCheck()
    except Exception as e:
        print(red(f"Ocurrió un error durante la ejecucion: {e}"))

if __name__ == "__main__":
    asyncio.run(main())

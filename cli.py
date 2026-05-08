import os

from dotenv import load_dotenv

import questionary

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.orders import OrderManager
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

from bot.logging_config import logger

# Rich console
console = Console()

# Load env
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")


def main():

    try:

        console.print(
            Panel.fit(
                "[bold cyan]BINANCE FUTURES TESTNET BOT[/bold cyan]",
                border_style="green"
            )
        )

        # User Inputs

        symbol = questionary.text(
            "Enter Symbol:",
            default="BTCUSDT"
        ).ask()

        side = questionary.select(
            "Choose Side:",
            choices=["BUY", "SELL"]
        ).ask()

        order_type = questionary.select(
            "Choose Order Type:",
            choices=["MARKET", "LIMIT"]
        ).ask()

        quantity = questionary.text(
            "Enter Quantity:",
            default="0.001"
        ).ask()

        price = None

        if order_type == "LIMIT":

            price = questionary.text(
                "Enter Limit Price:",
                default="50000"
            ).ask()

        # Validations

        symbol = symbol.upper()

        side = validate_side(side)

        order_type = validate_order_type(order_type)

        quantity = validate_quantity(quantity)

        price = validate_price(price, order_type)

        # Request Table

        request_table = Table(
            title="Order Request",
            show_header=True,
            header_style="bold magenta"
        )

        request_table.add_column("Field")
        request_table.add_column("Value")

        request_table.add_row("Symbol", symbol)
        request_table.add_row("Side", side)
        request_table.add_row("Order Type", order_type)
        request_table.add_row("Quantity", str(quantity))

        if price:
            request_table.add_row("Price", str(price))

        console.print(request_table)

        # Confirm Order

        confirm = questionary.confirm(
            "Do you want to place this order?",
            default=True
        ).ask()

        if not confirm:

            console.print(
                "\n[yellow]Order cancelled by user.[/yellow]"
            )

            return

        # Loading Spinner

        with console.status(
            "[bold green]Sending order to Binance Futures...[/bold green]"
        ):

            manager = OrderManager(API_KEY, API_SECRET)

            response = manager.execute_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

        # Response Table

        response_table = Table(
            title="Order Response",
            show_header=True,
            header_style="bold green"
        )

        response_table.add_column("Field")
        response_table.add_column("Value")

        response_table.add_row(
            "Order ID",
            str(response.get("orderId"))
        )

        response_table.add_row(
            "Status",
            str(response.get("status"))
        )

        response_table.add_row(
            "Executed Quantity",
            str(response.get("executedQty"))
        )

        response_table.add_row(
            "Average Price",
            str(response.get("avgPrice"))
        )

        console.print(response_table)

        console.print(
            Panel.fit(
                "[bold green]SUCCESS: Order placed successfully[/bold green]",
                border_style="green"
            )
        )

        logger.info("Order placed successfully")

    except Exception as e:

        console.print(
            Panel.fit(
                f"[bold red]ERROR:[/bold red] {e}",
                border_style="red"
            )
        )

        logger.error(f"CLI Error: {e}")


if __name__ == "__main__":
    main()
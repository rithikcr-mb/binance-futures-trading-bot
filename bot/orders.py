from bot.client import BinanceFuturesClient


class OrderManager:

    def __init__(self, api_key, api_secret):
        self.client = BinanceFuturesClient(
            api_key,
            api_secret
        )

    def execute_order(
        self,
        symbol,
        side,
        order_type,
        quantity,
        price=None
    ):

        response = self.client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        return response
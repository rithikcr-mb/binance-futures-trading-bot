from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger


class BinanceFuturesClient:

    def __init__(self, api_key, api_secret):

        try:
            self.client = Client(api_key, api_secret, testnet=True)

            # Futures Testnet URL
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

            logger.info("Binance Futures Testnet Client initialized")

        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise

    def place_order(
        self,
        symbol,
        side,
        order_type,
        quantity,
        price=None
    ):

        try:

            logger.info(
                f"Placing order | "
                f"Symbol={symbol} | "
                f"Side={side} | "
                f"Type={order_type} | "
                f"Qty={quantity} | "
                f"Price={price}"
            )

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                params["price"] = price
                params["timeInForce"] = "GTC"

            response = self.client.futures_create_order(**params)

            logger.info(f"Order Response: {response}")

            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise
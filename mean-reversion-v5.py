import numpy as np
import pandas as pd
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

class Trader:

    def __init__(self):
        self.price_history = {'PEARLS': [], 'BANANAS': []}
        self.position = {'PEARLS': 0, 'BANANAS': 0}
        self.position_age = {'PEARLS': 0, 'BANANAS': 0}
        self.position_limit = 20

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        for product in state.order_depths.keys():

            if product in ['PEARLS', 'BANANAS']:
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                # price = state.last_prices[product]
                best_bid, best_ask = None, None
                if order_depth.buy_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                if order_depth.sell_orders:
                    best_ask = min(order_depth.sell_orders.keys())
                # If both best bid and best ask exist
                if best_bid is not None and best_ask is not None:
                    # Calculate the mid price and check if it's profitable to trade
                    mid_price = (best_bid + best_ask) / 2

                price = mid_price

                self.price_history[product].append(price)

                if len(self.price_history[product]) >= 3:  # Adjust this value to use more time steps
                    recent_prices = pd.Series(self.price_history[product][-3:])
                    mean = recent_prices.mean()
                    std = recent_prices.std()
                    # buy
                    if price < mean - std:
                        buy_volume = min(abs(self.position_limit - self.position[product]), self.position_limit)
                        if buy_volume > 0:
                            orders.append(Order(product, price, buy_volume))
                            self.position[product] += buy_volume
                            self.position_age[product] = 0

                    # short here
                    elif price > mean + std:
                        sell_volume = min(self.position_limit, abs(self.position_limit + self.position[product]))
                        if sell_volume > 0:
                            orders.append(Order(product, price, -sell_volume))
                            self.position[product] -= sell_volume
                            self.position_age[product] = 0

                    elif abs(price - mean) <= 0.3 * std or self.position_age[product] >= 6:
                        if self.position[product] > 0:
                            orders.append(Order(product, price, -self.position[product]))
                            self.position[product] = 0
                            self.position_age[product] = 0
                        elif self.position[product] < 0:
                            orders.append(Order(product, price, abs(self.position[product])))
                            self.position[product] = 0
                            self.position_age[product] = 0
                    else:
                        self.position_age[product] += 1

                result[product] = orders

        return result

import configparser
import logging

import discord
import yfinance as yf
from discord.ext import commands

from stonkmaster.util.market_utils import is_market_closed


class PriceCommand(commands.Cog,
                   name="Price",
                   description="Shows the current price of the stonk, as well as its daily change."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @commands.command(name="price")
    async def _price(self, ctx, ticker):
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to fetch price for invalid ticker {ticker}")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            current = info['regularMarketPrice']
            previous = info['previousClose']
            symbol = info['symbol']
            change = ((current - previous) / previous) * 100
            emoji = self.config['emojis']['StockUp'] if change >= 0 else self.config['emojis']['StockDown']

            if 'longName' in info:
                msg = (f"The market price of **{info['longName']} ({symbol})** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")
            else:
                msg = (f"The market price of **{symbol}** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")

            logging.info(f"{ctx.author.display_name} fetched price for ticker {symbol} (current={current}, " +
                         f"previous={previous}, change={change}%)")
            await ctx.send(msg)

            if is_market_closed():
                await ctx.send(f"Market is currently **closed** {self.config['emojis']['Closed']}")
            elif symbol == 'GME':
                await ctx.send(f"Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: <https://gmefloor.com/> {self.config['emojis']['Money']}")
                await ctx.send(f"Weitere Infos findst do: <https://gme.crazyawesomecompany.com/> {self.config['emojis']['Bulb']}")

        except Exception as ex:
            logging.error(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")

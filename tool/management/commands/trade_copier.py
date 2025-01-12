from django.core.management.base import BaseCommand
from tool.models import copier_details, master_details, server_details
import MetaTrader5 as mt5
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Trade copier to replicate trades from master to slave accounts"

    def handle(self, *args, **kwargs):
        # Fetch all copier accounts
        copiers = copier_details.objects.select_related('master', 'server').all()

        for copier in copiers:
            # Extract server details
            server = copier.server
            master = copier.master

            if not server or not master:
                logger.warning(f"Skipping copier ID {copier.id} due to missing server or master details.")
                continue

            server_ip = server.server_ip

            # Extract master account details
            master_mt5_id = master.mt5_id
            master_password = master.password
            master_server_name = server.server_name

            # Extract copier (slave) account details
            copier_mt5_id = copier.mt5_id
            copier_password = copier.password

            logger.info(f"Processing copier ID {copier.id} for Master ID {master_mt5_id} on server {server_ip}")

            # Connect to the master account
            if not self.connect_to_mt5(master_mt5_id, master_password, master_server_name):
                logger.error(f"Failed to connect to master account {master_mt5_id}. Skipping copier ID {copier.id}.")
                continue

            # Fetch trades from the master account
            master_trades = mt5.positions_get()
            if master_trades is None:
                logger.warning(f"No trades found for master account {master_mt5_id}.")
                mt5.shutdown()
                continue

            logger.info(f"Found {len(master_trades)} trades for master account {master_mt5_id}.")

            # Connect to the copier (slave) account
            if not self.connect_to_mt5(copier_mt5_id, copier_password, master_server_name):
                logger.error(f"Failed to connect to copier account {copier_mt5_id}. Skipping.")
                mt5.shutdown()
                continue

            # Copy trades to the copier account
            self.copy_trades_to_slave(master_trades, copier)

            # Disconnect from MetaTrader 5
            mt5.shutdown()

    def connect_to_mt5(self, login, password, server):
        """Connect to a MetaTrader 5 account."""
        mt5.shutdown()  # Ensure any previous connection is closed
        if mt5.initialize(login=login, password=password, server=server):
            logger.info(f"Successfully connected to account {login}.")
            return True
        else:
            logger.error(f"Failed to connect to account {login}. Error: {mt5.last_error()}")
            return False

    def copy_trades_to_slave(self, trades, copier):
        """Copy trades from the master account to the slave account."""
        for trade in trades:
            symbol_info = mt5.symbol_info(trade.symbol)
            if not symbol_info:
                logger.error(f"Symbol {trade.symbol} not found.")
                continue

            # Ensure the symbol is enabled in the market watch
            if not symbol_info.visible:
                if not mt5.symbol_select(trade.symbol, True):
                    logger.error(f"Failed to select symbol {trade.symbol}.")
                    continue

            trade_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": trade.symbol,
                "volume": trade.volume,
                "type": trade.type,
                "price": mt5.symbol_info_tick(trade.symbol).ask,
                "sl": trade.sl if copier.stop_loss else 0.0,
                "tp": trade.tp if copier.take_profit else 0.0,
                "deviation": 10,
                "magic": 234000,  # You can set a unique magic number for identification
                "comment": "Trade copied by Django trade copier",
            }

            logger.debug(f"Trade request: {trade_request}")

            # Send the trade request
            result = mt5.order_send(trade_request)
            if result is None:
                logger.error("Failed to send trade request: mt5.order_send returned None.")
                logger.error(f"Check the trade request: {trade_request}")
                continue

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Failed to copy trade {trade.symbol} for copier {copier.mt5_id}. Error: {result.retcode}")
            else:
                logger.info(f"Successfully copied trade {trade.symbol} to copier {copier.mt5_id}.")


import click
from datetime import datetime
from portfolio.data import load_data, save_data, init_data

@click.group()
def cli():
    """📈 Stock Portfolio Tracker CLI"""
    init_data()

@cli.command()
def add():
    """➕ Add a stock to your portfolio"""
    symbol = click.prompt("Enter stock symbol", type=str).upper()
    quantity = click.prompt("Enter quantity", type=float)
    buy_price = click.prompt("Enter buy price per share", type=float)
    buy_date = click.prompt("Enter buy date (YYYY-MM-DD)", default=datetime.today().strftime("%Y-%m-%d"))

    holding = {
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price,
        "buy_date": buy_date
    }

    data = load_data()
    data["holdings"].append(holding)

    # Log transaction
    data["history"].append({
        "action": "add",
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price,
        "date": buy_date
    })

    save_data(data)
    click.secho(f"✅ Added {quantity} shares of {symbol} at ₹{buy_price}", fg="green")


@cli.command()
@click.argument("symbol")
def remove(symbol):
    """➖ Remove a stock from your portfolio by symbol"""
    symbol = symbol.upper()
    data = load_data()
    holdings = data["holdings"]
    new_holdings = [h for h in holdings if h["symbol"] != symbol]

    if len(new_holdings) == len(holdings):
        click.secho(f"❌ No stock with symbol {symbol} found.", fg="red")
        return

    removed = [h for h in holdings if h["symbol"] == symbol]
    data["holdings"] = new_holdings

    # Log removal
    for h in removed:
        data["history"].append({
            "action": "removed",
            "symbol": h["symbol"],
            "quantity": h["quantity"],
            "buy_price": h["buy_price"],
            "date": datetime.today().strftime("%Y-%m-%d")
        })

    save_data(data)
    click.secho(f"✅ Removed {symbol} from portfolio", fg="yellow")
from tabulate import tabulate

@cli.command()
def view():
    """👀 View current portfolio"""
    data = load_data()
    holdings = data["holdings"]
    if not holdings:
        click.secho("📭 Portfolio is empty.", fg="yellow")
        return
    
    table = [
        [h['symbol'], h['quantity'], h['buy_price'], h['buy_date']]
        for h in holdings
    ]
    headers = ["Symbol", "Quantity", "Buy Price", "Buy Date"]
    click.echo(tabulate(table, headers, tablefmt="pretty"))

@cli.command()
def history():
    """📜 View transaction history"""
    data = load_data()
    history = data["history"]
    if not history:
        click.secho("📭 No transaction history found.", fg="yellow")
        return
    
    table = [
        [h['action'], h['symbol'], h['quantity'], h['buy_price'], h['date']]
        for h in history
    ]
    headers = ["Action", "Symbol", "Quantity", "Buy Price", "Date"]
    click.echo(tabulate(table, headers, tablefmt="pretty"))

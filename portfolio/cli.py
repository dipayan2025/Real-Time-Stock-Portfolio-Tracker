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
    if not symbol.endswith(".NS") and len(symbol) <= 5:
        symbol += ".NS"
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
    if not symbol.endswith(".NS") and len(symbol) <= 5:
        symbol += ".NS"
    data = load_data()
    holdings = data["holdings"]
    new_holdings = [h for h in holdings if h["symbol"] != symbol]

    if len(new_holdings) == len(holdings):
        click.secho(f"❌ No stock with symbol {symbol} found.", fg="red")
        return

    removed = [h for h in holdings if h["symbol"] == symbol]
    data["holdings"] = new_holdings

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

from portfolio.pricing import get_current_price
from tabulate import tabulate

@cli.command()
def view():
    """👀 View current portfolio with gain/loss"""
    data = load_data()
    holdings = data["holdings"]
    if not holdings:
        click.secho("📭 Portfolio is empty.", fg="yellow")
        return
    
    table = []
    total_value = 0
    total_gain = 0
    for h in holdings:
        symbol = h["symbol"]
        quantity = h["quantity"]
        buy_price = h["buy_price"]
        current_price = get_current_price(symbol)
        
        if current_price is None:
            click.secho(f"⚠️ Could not fetch current price for {symbol}", fg="red")
            continue
        
        market_value = quantity * current_price
        gain_loss_pct = ((current_price - buy_price) / buy_price) * 100
        
        table.append([
            symbol,
            quantity,
            f"₹{buy_price:.2f}",
            f"₹{current_price:.2f}",
            f"₹{market_value:.2f}",
            f"{gain_loss_pct:.2f}%"
        ])
        
        total_value += market_value
        total_gain += gain_loss_pct

    headers = ["Symbol", "Quantity", "Buy Price", "Current Price", "Market Value", "% Gain/Loss"]
    click.echo(tabulate(table, headers, tablefmt="pretty"))

    avg_gain = total_gain / len(holdings) if holdings else 0
    click.secho(f"\n💰 Total Portfolio Value: ₹{total_value:.2f}", fg="green", bold=True)
    click.secho(f"📈 Average Gain/Loss: {avg_gain:.2f}%", fg="cyan", bold=True)

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

from portfolio.cli import cli
import click

def menu():
    while True:
        click.secho("\n📈 Stock Portfolio Tracker", fg="cyan", bold=True)
        click.echo("1. Add Stock")
        click.echo("2. Remove Stock")
        click.echo("3. View Portfolio")
        click.echo("4. View History")
        click.echo("5. Exit")
        choice = click.prompt("Select an option", type=int)

        ctx = click.Context(cli)

        if choice == 1:
            cli.commands["add"].invoke(ctx)
        elif choice == 2:
            symbol = click.prompt("Enter symbol to remove", type=str)
            cli.commands["remove"].invoke(ctx, [symbol])   # <-- fix here
        elif choice == 3:
            cli.commands["view"].invoke(ctx)
        elif choice == 4:
            cli.commands["history"].invoke(ctx)
        elif choice == 5:
            click.secho("👋 Goodbye!", fg="yellow")
            break
        else:
            click.secho("❌ Invalid choice", fg="red")

if __name__ == "__main__":
    menu()

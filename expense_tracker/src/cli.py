import expense_tracker as et
from datetime import datetime
import click

@click.group()
def cli():
    pass

@cli.command('add')
@click.option("--amount", "-a", required=True, type=click.FloatRange(min=0.01), help="Transaction amount.")
@click.option("-c", "--category", default='misc', help="Expense category (default is misc)")
@click.option(
    "-d", "--date",
    type=click.DateTime(["%Y-%m-%d"]),
    default=None,
    help="Date in YYYY-MM-DD format (defaults to today)"
)
def add_transaction(date: str, amount: float, category: str) -> None:
    """Add a transaction to the ledger"""
    dt = date or datetime.now()
    date_str = dt.strftime("%Y-%m-%d")
    et.add_transaction(date_str, amount, category)
    print(f'Transaction added [{date_str}, {amount}, {category}]')


@cli.command('summary')
@click.option(
    "-o", "--option",
    required=True,
    type=click.Choice(["month", "year"], False),
    help="Summary period")
def generate_summary(option: str) -> None:
    """generates summary grouped by category"""
    summary = et.generate_summary(option)

    if not summary:
        print("No entries detected.")
        return


    print(f"{f" Summary: {option.upper()} ".center(50, "-")}")

    for item in summary:
        print(item)
    
    print(f"{'_'.center(50, "_")}")

if __name__ == "__main__":
    cli()
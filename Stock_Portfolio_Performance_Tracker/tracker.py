import csv
from datetime import datetime
from pathlib import Path

import yfinance as yf

# File locations
BASE_DIR = Path(__file__).resolve().parent
STOCK_FILE = BASE_DIR / "constituents.csv"
LOG_FILE = BASE_DIR / "portfolio_summary.csv"

# CSV column headings
HEADERS = [
    "Timestamp", "Symbol", "Company", "Sector", "Shares",
    "Buy Price (USD)", "Current Price (USD)", "Invested (USD)",
    "Market Value (USD)", "Gain/Loss (USD)", "Gain/Loss (%)"
]


# Read stock information from constituents.csv
def load_stocks():
    stocks = {}

    with STOCK_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            symbol = row["Symbol"].strip().upper()

            stocks[symbol] = {
                "company": row["Security"].strip(),
                "sector": row["GICS Sector"].strip()
            }

    return stocks


# Ask the user to enter a valid positive number
def ask_positive_number(message):
    while True:
        try:
            value = float(input(message).strip())

            if value > 0 and value != float("inf"):
                return value

        except ValueError:
            pass

        print("  Please enter a valid number greater than zero.")


# Get the latest available stock price from Yahoo Finance
def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol.replace(".", "-"))
        history = ticker.history(period="5d", auto_adjust=False)

        if history.empty:
            return None

        price = float(history["Close"].dropna().iloc[-1])

        if price > 0 and price != float("inf"):
            return price

        return None

    except Exception as error:
        print(f"  Could not retrieve {symbol}: {error}")
        return None


# Save portfolio information to portfolio_summary.csv
def save_summary(holdings, totals):

    # Check whether the file already exists or is empty
    needs_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write column headings if the file is empty
        if needs_header:
            writer.writerow(HEADERS)

        # Save information about each stock
        for item in holdings:
            writer.writerow([
                timestamp,
                item["symbol"],
                item["company"],
                item["sector"],
                item["shares"],
                f'{item["buy_price"]:.2f}',
                f'{item["current_price"]:.2f}',
                f'{item["invested"]:.2f}',
                f'{item["value"]:.2f}',
                f'{item["gain"]:.2f}',
                f'{item["gain_percent"]:.2f}'
            ])

        # Save the total portfolio information
        writer.writerow([
            timestamp,
            "TOTAL",
            "PORTFOLIO",
            "",
            "",
            "",
            "",
            f'{totals["invested"]:.2f}',
            f'{totals["value"]:.2f}',
            f'{totals["gain"]:.2f}',
            f'{totals["gain_percent"]:.2f}'
        ])


# Display portfolio information and calculate totals
def display_portfolio(holdings):

    total_invested = 0
    total_value = 0

    # Calculate total invested amount and market value
    for item in holdings:
        total_invested += item["invested"]
        total_value += item["value"]

    total_gain = total_value - total_invested
    total_percent = (total_gain / total_invested) * 100

    # Display portfolio information
    print("\n" + "=" * 92)
    print("                 STOCK PORTFOLIO PERFORMANCE")
    print("=" * 92)

    print(
        f'{"SYMBOL":<10}{"SHARES":>10}{"BUY $":>13}'
        f'{"NOW $":>13}{"VALUE $":>16}{"P/L $":>16}{"P/L %":>14}'
    )

    print("-" * 92)

    for item in holdings:
        print(
            f'{item["symbol"]:<10}'
            f'{item["shares"]:>10.2f}'
            f'{item["buy_price"]:>13.2f}'
            f'{item["current_price"]:>13.2f}'
            f'{item["value"]:>16.2f}'
            f'{item["gain"]:>+16.2f}'
            f'{item["gain_percent"]:>+13.2f}%'
        )

    print("-" * 92)

    print(f"  Total invested : ${total_invested:,.2f}")
    print(f"  Current value  : ${total_value:,.2f}")
    print(f"  Overall P/L    : ${total_gain:+,.2f} ({total_percent:+.2f}%)")

    print("=" * 92)

    return {
        "invested": total_invested,
        "value": total_value,
        "gain": total_gain,
        "gain_percent": total_percent
    }


# Main program
def main():

    print("\n" + "=" * 55)
    print("       STOCKSCOPE | Portfolio Performance Tracker")
    print("=" * 55)

    print("  S&P 500 stocks | Latest available market prices")

    # Load stock information
    try:
        stocks = load_stocks()

    except (OSError, KeyError, csv.Error) as error:
        print(f"Could not read constituents.csv: {error}")
        return

    holdings = []

    # Take stock information from the user
    while True:

        symbol = input("\nStock symbol (or DONE to finish): ").strip().upper()

        if symbol == "DONE":
            break

        # Check whether the entered symbol exists
        if symbol not in stocks:
            print("  Symbol not found in the provided S&P 500 dataset. Try again.")
            continue

        # Prevent adding the same stock twice
        duplicate = False

        for item in holdings:
            if item["symbol"] == symbol:
                duplicate = True
                break

        if duplicate:
            print("  Already added this symbol. Enter another stock.")
            continue

        print(f'  Found: {stocks[symbol]["company"]} | {stocks[symbol]["sector"]}')

        # Get buying price and number of shares
        buy_price = ask_positive_number("  Your buy price per share (USD): $")
        shares = ask_positive_number("  Number of shares: ")

        # Get the latest available stock price
        print("  Looking up latest available price...")

        current_price = get_price(symbol)

        if current_price is None:
            print("  Price unavailable. This stock was not added; please try later.")
            continue

        # Calculate stock performance
        invested = buy_price * shares
        value = current_price * shares
        gain = value - invested
        gain_percent = (gain / invested) * 100

        # Store the stock information
        holdings.append({
            "symbol": symbol,
            "company": stocks[symbol]["company"],
            "sector": stocks[symbol]["sector"],
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "value": value,
            "gain": gain,
            "gain_percent": gain_percent
        })

        print(f"  Added {symbol}! Latest available price: ${current_price:,.2f}")

    # Check whether the user added any stocks
    if not holdings:
        print("\nNo holdings added. Nothing to save.")
        return

    # Display portfolio performance
    totals = display_portfolio(holdings)

    # Save portfolio information to CSV
    try:
        save_summary(holdings, totals)
        print(f"\n  Saved performance log to: {LOG_FILE.name}")

    except OSError as error:
        print(f"\n  Could not save the CSV log: {error}")

    print("  Note: Market data may be delayed; not a live trading feed.")


# Start the program
if __name__ == "__main__":
    main()

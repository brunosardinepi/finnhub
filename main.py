import argparse
import csv
import finnhub


def create_csv(client, symbol, type):
    # Get the financials.
    financials = client.financials(symbol, type, 'quarterly')

    # Isolate the column names from the Client response.
    columns = []
    for dict in financials['financials']:
        for key, value in dict.items():
            if key not in columns:
                columns.append(key)
    print(f"Columns: {columns}")

    # Loop through financials and add to CSV.
    data = []
    for dict in financials['financials']:
        values = []
        for column in columns:
            if column in dict:
                values.append(dict[column])
            else:
                values.append('')
        data.append(values)

    with open(f"{symbol}_{type}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)

def main():
    # Get CLI args.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--symbol',
        type=str,
        required=True,
        help="The stock symbol of the company",
    )
    args = parser.parse_args()

    # Get the stock symbol.
    symbol = args.symbol.split(";")[0].strip()

    # Create a new Client object.
    c = finnhub.Client(api_key="sandbox_c620d3aad3iccpc4ang0")

    create_csv(c, symbol, 'cf')
    create_csv(c, symbol, 'ic')
    create_csv(c, symbol, 'bs')

if __name__ == "__main__":
    main()

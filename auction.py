import json

# 1. The input data (JSON string format)
# This mimics the "Alice, Bob, Bib ID" structure you mentioned.
json_data = """
[
    {"id": "b1", "bidder": "Alice", "amount": 100},
    {"id": "b2", "bidder": "Bob",   "amount": 90},
    {"id": "b3", "bidder": "Charlie","amount": 110},
    {"id": "b4", "bidder": "Dave",  "amount": 105}
]
"""


def run_auction_from_json(json_input):
    # Parse the JSON string into a Python list of dictionaries
    bids = json.loads(json_input)

    print(f"--- Received {len(bids)} Bids ---")
    for b in bids:
        print(f"ID: {b['id']} | Bidder: {b['bidder']} | Amount: {b['amount']}")

    # Logic: Sort bids by amount in descending order (highest first)
    # We use a lambda function to tell the sort to look at the 'amount' key
    sorted_bids = sorted(bids, key=lambda x: x['amount'], reverse=True)

    # Determine Winner (Highest Bid)
    winner = sorted_bids[0]

    # Determine Price (Second Highest Bid) - Vickrey Auction style
    # If there is only one bidder, they pay their own price (or a reserve)
    if len(sorted_bids) > 1:
        second_highest = sorted_bids[1]
        payment = second_highest['amount']
    else:
        payment = winner['amount']

    print("\n--- Auction Results ---")
    print(f"Winner: {winner['bidder']} (Bid: {winner['amount']})")
    print(f"Price to Pay: {payment}")
    print(f"Winning Bid ID: {winner['id']}")


# Run the function
run_auction_from_json(json_data)
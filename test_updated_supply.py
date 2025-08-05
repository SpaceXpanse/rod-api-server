import requests
import json

# Test the updated supply calculation
response = requests.get("http://localhost:1234/supply")
data = response.json()

print("Updated Supply Calculation:")
print("=" * 40)
print(f"Current supply: {data['result']['supply'] / 100000000:,.2f} ROD")
print(f"Max supply: {data['result']['total/max supply'] / 100000000:,.2f} ROD")
print(f"Halvings: {data['result']['halvings']}")

# Compare with Coinpaprika data
coinpaprika_total_supply = 1569062124
coinpaprika_max_supply = 4615066365

print(f"\nComparison with Coinpaprika:")
print(f"Coinpaprika total supply: {coinpaprika_total_supply:,} ROD")
print(f"Coinpaprika max supply: {coinpaprika_max_supply:,} ROD")
print(f"Our max supply: {data['result']['total/max supply'] / 100000000:,.2f} ROD")
print(f"Difference: {abs(coinpaprika_max_supply - data['result']['total/max supply'] / 100000000):,.2f} ROD")
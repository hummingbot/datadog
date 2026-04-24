#!/usr/bin/env python3
"""Export Hummingbot volume data from Datadog for the past year."""

import os
import requests
import csv
import time
from datetime import datetime, timedelta

# Datadog credentials - set via environment variables
API_KEY = os.environ.get("DD_API_KEY", "")
APP_KEY = os.environ.get("DD_APP_KEY", "")
DATADOG_SITE = os.environ.get("DD_SITE", "datadoghq.com")

# Time range: 15 months ago (max Datadog retention) to now
end_time = int(time.time())
start_time = int((datetime.now() - timedelta(days=456)).timestamp())  # ~15 months ago

# Base URL
BASE_URL = f"https://api.{DATADOG_SITE}"

headers = {
    "DD-API-KEY": API_KEY,
    "DD-APPLICATION-KEY": APP_KEY,
    "Content-Type": "application/json"
}

def query_metrics(query: str, from_ts: int, to_ts: int) -> dict:
    """Query Datadog metrics API."""
    url = f"{BASE_URL}/api/v1/query"
    params = {
        "query": query,
        "from": from_ts,
        "to": to_ts
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def extract_tag_value(scope: str, tag_name: str) -> str:
    """Extract the clean tag value from a Datadog scope string."""
    # Scope looks like: "exchange:binance,!altmarkets,!kraken_perpetual,..."
    # We want just "binance"
    parts = scope.split(",")
    for part in parts:
        if part.startswith(f"{tag_name}:"):
            return part.replace(f"{tag_name}:", "")
    return scope

def export_volume_by_exchange():
    """Export daily volume by exchange connector."""
    print("Fetching volume data by exchange...")

    query = "sum:hummingbot.filled_usdt_volume{!exchange:*testnet,!exchange:altmarkets,!exchange:mcx_perpetual,!exchange:*sepolia,!exchange:lbank,!exchange:kraken_perpetual,!exchange:uae*,!exchange:yamata,!exchange:polymarket/ctf,!exchange:pancakeswap_binance-smart-chain_mainnet,!exchange:deribit_perpetual,!exchange:ekiden_perpetual} by {exchange}.rollup(sum, 86400)"

    data = query_metrics(query, start_time, end_time)

    rows = []
    if "series" in data:
        for series in data["series"]:
            exchange = extract_tag_value(series.get("scope", "unknown"), "exchange")
            pointlist = series.get("pointlist", [])
            for point in pointlist:
                timestamp_ms, value = point
                if value is not None:
                    dt = datetime.fromtimestamp(timestamp_ms / 1000)
                    rows.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "exchange": exchange,
                        "volume_usdt": value
                    })

    # Sort by date and exchange
    rows.sort(key=lambda x: (x["date"], x["exchange"]))

    # Write to CSV
    output_file = "/Users/feng/fengtality/datadog/volume_by_exchange.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "exchange", "volume_usdt"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {output_file}")
    return rows

def export_volume_by_version():
    """Export daily volume by version."""
    print("Fetching volume data by version...")

    query = "sum:hummingbot.filled_usdt_volume{!exchange:*testnet,!exchange:altmarkets,!exchange:mcx_perpetual,!exchange:*sepolia,!exchange:lbank,!exchange:kraken_perpetual,!exchange:uae*,!exchange:yamata,!exchange:polymarket/ctf,!exchange:pancakeswap_binance-smart-chain_mainnet,!exchange:deribit_perpetual,!exchange:ekiden_perpetual} by {version}.rollup(sum, 86400)"

    data = query_metrics(query, start_time, end_time)

    rows = []
    if "series" in data:
        for series in data["series"]:
            version = extract_tag_value(series.get("scope", "unknown"), "version")
            pointlist = series.get("pointlist", [])
            for point in pointlist:
                timestamp_ms, value = point
                if value is not None:
                    dt = datetime.fromtimestamp(timestamp_ms / 1000)
                    rows.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "version": version,
                        "volume_usdt": value
                    })

    rows.sort(key=lambda x: (x["date"], x["version"]))

    output_file = "/Users/feng/fengtality/datadog/volume_by_version.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "version", "volume_usdt"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {output_file}")
    return rows

def export_volume_by_instance():
    """Export daily volume by instance."""
    print("Fetching volume data by instance...")

    query = "sum:hummingbot.filled_usdt_volume{!exchange:*testnet,!exchange:altmarkets,!exchange:mcx_perpetual,!exchange:*sepolia,!exchange:lbank,!exchange:kraken_perpetual,!exchange:uae*,!exchange:yamata,!exchange:polymarket/ctf,!exchange:pancakeswap_binance-smart-chain_mainnet,!exchange:deribit_perpetual,!exchange:ekiden_perpetual} by {instance_id}.rollup(sum, 86400)"

    data = query_metrics(query, start_time, end_time)

    rows = []
    if "series" in data:
        for series in data["series"]:
            instance_id = extract_tag_value(series.get("scope", "unknown"), "instance_id")
            pointlist = series.get("pointlist", [])
            for point in pointlist:
                timestamp_ms, value = point
                if value is not None:
                    dt = datetime.fromtimestamp(timestamp_ms / 1000)
                    rows.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "instance_id": instance_id,
                        "volume_usdt": value
                    })

    rows.sort(key=lambda x: (x["date"], x["instance_id"]))

    output_file = "/Users/feng/fengtality/datadog/volume_by_instance.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "instance_id", "volume_usdt"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {output_file}")
    return rows

def export_total_daily_volume():
    """Export total daily volume."""
    print("Fetching total daily volume...")

    query = "sum:hummingbot.filled_usdt_volume{!exchange:*testnet,!exchange:altmarkets,!exchange:mcx_perpetual,!exchange:*sepolia,!exchange:lbank,!exchange:kraken_perpetual,!exchange:uae*,!exchange:yamata,!exchange:polymarket/ctf,!exchange:pancakeswap_binance-smart-chain_mainnet,!exchange:deribit_perpetual,!exchange:ekiden_perpetual}.rollup(sum, 86400)"

    data = query_metrics(query, start_time, end_time)

    rows = []
    if "series" in data:
        for series in data["series"]:
            pointlist = series.get("pointlist", [])
            for point in pointlist:
                timestamp_ms, value = point
                if value is not None:
                    dt = datetime.fromtimestamp(timestamp_ms / 1000)
                    rows.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "total_volume_usdt": value
                    })

    rows.sort(key=lambda x: x["date"])

    output_file = "/Users/feng/fengtality/datadog/total_daily_volume.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "total_volume_usdt"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {output_file}")
    return rows

if __name__ == "__main__":
    print(f"Exporting data from {datetime.fromtimestamp(start_time)} to {datetime.fromtimestamp(end_time)}")
    print("-" * 50)

    export_total_daily_volume()
    export_volume_by_exchange()
    export_volume_by_version()
    export_volume_by_instance()

    print("-" * 50)
    print("Export complete!")

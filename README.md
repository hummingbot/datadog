# Hummingbot Reported Volumes

Interactive dashboard visualizing aggregated trading volumes reported by Hummingbot instances worldwide.

**Live Dashboard:** [View on GitHub Pages](https://hummingbot.github.io/datadog/) *(coming soon)*

## About the Data

This dashboard displays anonymized metrics collected from Hummingbot trading bot instances. As described in the [Hummingbot Reporting documentation](https://hummingbot.org/reporting/):

- Hummingbot instances report aggregated metrics every 15 minutes via HTTPS
- Data is **fully anonymized** — no personal information, wallet addresses, or API keys are collected
- Each instance is identified only by a random UUID to prevent duplicate counting
- All data is aggregated before public display

### What's Reported

| Metric | Description |
|--------|-------------|
| Trade Volume | Aggregated USD volume totals |
| Exchange | Connector identifier (e.g., `binance`, `uniswap`) |
| Version | Hummingbot version for adoption tracking |
| Instance ID | Random UUID (anonymized) |

### Opt-Out

Users can disable reporting by running:
```
config anonymized_metrics_enabled False
```

## Dashboard Features

- **Filter by Time Range**: All time, last 30/90/180/365 days, or custom date range
- **Filter by Exchange**: Multi-select dropdown with search
- **Interactive Charts**: Zoom, pan, and export capabilities
- **Exchange Rankings**: Sortable table with volume share percentages

## Data Files

| File | Description |
|------|-------------|
| `total_daily_volume.csv` | Daily aggregated volume across all exchanges |
| `volume_by_exchange.csv` | Daily volume broken down by exchange connector |
| `volume_by_version.csv` | Daily volume broken down by Hummingbot version |

## Refreshing Data

Data is exported from Datadog using the included script. Requires Datadog API credentials:

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
python3 export_data.py
```

## Development

```bash
# Install dependencies
npm install

# Start local server
python3 -m http.server 8080

# Run tests
npx playwright test
```

## License

This project is part of the [Hummingbot](https://hummingbot.org) ecosystem — the open source framework for crypto market makers.

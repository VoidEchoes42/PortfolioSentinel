import pandas as pd
from datetime import datetime
from config.settings import THRESHOLDS


def check_market_alerts(market_metrics: dict) -> list:
    """
    Checks market metrics against thresholds and generates alerts.
    Expected keys in market_metrics: 'volatility', 'drawdown', 'var_95'.
    """
    alerts = []

    if market_metrics.get("volatility", 0) > THRESHOLDS["volatility_critical"]:
        alerts.append(
            {
                "category": "Market Risk",
                "severity": "Critical",
                "message": f"Portfolio volatility has reached a critical level ({market_metrics['volatility']:.1%}).",
                "timestamp": datetime.now().isoformat(),
            }
        )
    elif market_metrics.get("volatility", 0) > THRESHOLDS["volatility_warning"]:
        alerts.append(
            {
                "category": "Market Risk",
                "severity": "Warning",
                "message": f"Portfolio volatility is elevated ({market_metrics['volatility']:.1%}).",
                "timestamp": datetime.now().isoformat(),
            }
        )

    if market_metrics.get("drawdown", 0) > THRESHOLDS["drawdown_critical"]:
        alerts.append(
            {
                "category": "Market Risk",
                "severity": "Critical",
                "message": f"Severe portfolio drawdown detected ({market_metrics['drawdown']:.1%}).",
                "timestamp": datetime.now().isoformat(),
            }
        )

    if market_metrics.get("var_95", 0) > THRESHOLDS["var_95_critical"]:
        alerts.append(
            {
                "category": "Market Risk",
                "severity": "Warning",
                "message": f"95% Value at Risk exceeds threshold ({market_metrics['var_95']:.1%}).",
                "timestamp": datetime.now().isoformat(),
            }
        )

    return alerts


def check_credit_alerts(credit_metrics: dict) -> list:
    """
    Checks credit portfolio metrics against thresholds.
    Expected keys: 'hhi', 'watchlist_count', 'avg_pd'
    """
    alerts = []

    if credit_metrics.get("hhi", 0) > THRESHOLDS["hhi_concentration"]:
        alerts.append(
            {
                "category": "Credit Risk",
                "severity": "Warning",
                "message": f"High sector concentration detected (HHI: {credit_metrics['hhi']:.3f}).",
                "timestamp": datetime.now().isoformat(),
            }
        )

    if credit_metrics.get("watchlist_count", 0) > 5:
        alerts.append(
            {
                "category": "Credit Risk",
                "severity": "Warning",
                "message": f"Watchlist has grown to {credit_metrics['watchlist_count']} borrowers.",
                "timestamp": datetime.now().isoformat(),
            }
        )

    return alerts


def get_top_risks(all_alerts: list, n: int = 5) -> list:
    """Sorts alerts by severity and returns the top N."""
    severity_rank = {"Critical": 0, "Warning": 1, "Watch": 2}
    sorted_alerts = sorted(
        all_alerts, key=lambda x: severity_rank.get(x["severity"], 99)
    )
    return sorted_alerts[:n]

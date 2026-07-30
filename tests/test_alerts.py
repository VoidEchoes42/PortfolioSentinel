from src.alerts.engine import check_credit_alerts, check_market_alerts, get_top_risks


def test_market_alert_critical_volatility():
    metrics = {"volatility": 0.35, "drawdown": 0.05, "var_95": 0.02}
    alerts = check_market_alerts(metrics)
    assert len(alerts) >= 1
    assert alerts[0]["severity"] == "Critical"


def test_market_alert_warning_volatility():
    metrics = {"volatility": 0.22, "drawdown": 0.05, "var_95": 0.02}
    alerts = check_market_alerts(metrics)
    assert len(alerts) >= 1
    assert alerts[0]["severity"] == "Warning"


def test_no_alerts_when_within_limits():
    metrics = {"volatility": 0.10, "drawdown": 0.03, "var_95": 0.01}
    alerts = check_market_alerts(metrics)
    assert len(alerts) == 0


def test_credit_alert_concentration():
    metrics = {"hhi": 0.30, "watchlist_count": 2}
    alerts = check_credit_alerts(metrics)
    assert any("concentration" in a["message"].lower() for a in alerts)


def test_get_top_risks_sorts_by_severity():
    alerts = [
        {"severity": "Warning", "category": "Market", "message": "vol"},
        {"severity": "Critical", "category": "Credit", "message": "pd"},
    ]
    top = get_top_risks(alerts, n=2)
    assert top[0]["severity"] == "Critical"

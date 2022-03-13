
"""
Send an Alert Event to PagerDuty
NOTE: "ALERT_ROUTING_KEY" environment variable must contain a
valid routing key for a PagerDuty service.
https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started
Usage:
    $ python -m pd_alert "Alert Title" "Alert Body" "dedup_key"
    or
    import pd_alert
    pd_alert.send_alert("Alert Title", "Alert Body", "Optional dedup key")
"""
import json
import logging
import os
from datetime import datetime
from http.client import HTTPSConnection
from typing import Any
from typing import Dict
from typing import Optional

__all__ = ["build_alert", "send_alert"]

ROUTING_KEY = " "  #os.getenv("ALERT_ROUTING_KEY")
log = logging.getLogger(__name__)


def build_alert(title: str, alert_body: str, dedup: str) -> Dict[str, Any]:
    """
    Builds the payload for an event alert.
    Args
        title: Title of alert
        alert_body: UTF-8 string of custom message for alert. Shown in incident body
        dedup: Any string, max 255, characters used to deduplicate alerts
    Returns
        Dictionary of alert body for JSON serialization
    """
    return {
        "routing_key": ROUTING_KEY,
        "event_action": "trigger",
        "dedup_key": dedup,
        "payload": {
            "summary": title,
            "source": "custom_event",
            "severity": "critical",
            "custom_details": {
                "alert_body": alert_body,
            },
        },
    }


def send_alert(title: str, alert_body: str, dedup: Optional[str] = None) -> None:
    """
    Sends PagerDuty Alert
    Args
        title: Title of the alert.
        alert_body: UTF-8 string of custom message for alert. Shown in incident body
        dedup: Any string, max 255, characters used to deduplicate alerts
    Returns
        None
    """
    # If no dedup is given, use epoch timestamp
    if dedup is None:
        dedup = str(datetime.utcnow().timestamp())
    url = "events.pagerduty.com"
    route = "/v2/enqueue"

    conn = HTTPSConnection(host=url, port=443)
    conn.request("POST", route, json.dumps(build_alert(title, alert_body, dedup)))
    result = conn.getresponse()

    log.info("Alert status: %s", result.status)
    log.info("Alert response: %s", result.read())


if __name__ == "__main__":
    # For CLI use
    import sys

    logging.basicConfig(level="INFO")
    if len(sys.argv) != 4:
        print('Use: python -m pd_alert "Alert Title" "Alert Body" "dedup_key"')
    send_alert(*sys.argv[1:])
    raise SystemExit(1)

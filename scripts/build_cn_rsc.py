#!/usr/bin/env python3

import datetime
import ipaddress
import re
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list"

OUT_RSC = Path("CN.rsc")
OUT_COUNT = Path("CN.count.txt")
OUT_SOURCE = Path("CN.source.txt")

CIDR_RE = re.compile(
    r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}/(?:[0-9]|[12][0-9]|3[0-2])(?![\d.])"
)


def download_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ros-cn-rules-builder/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def main() -> None:
    raw = download_text(SOURCE_URL)

    networks = []
    for item in CIDR_RE.findall(raw):
        try:
            net = ipaddress.ip_network(item, strict=False)
            if isinstance(net, ipaddress.IPv4Network):
                networks.append(net)
        except ValueError:
            continue

    networks = sorted(
        ipaddress.collapse_addresses(networks),
        key=lambda n: int(n.network_address),
    )

    if len(networks) < 3000:
        raise RuntimeError(f"CN IPv4 network count too small: {len(networks)}")

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    with OUT_RSC.open("w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Generated at: {now}\n")
        f.write(f"# Source: {SOURCE_URL}\n")
        f.write(f"# Count: {len(networks)}\n")
        f.write("/ip firewall address-list\n")
        for net in networks:
            f.write(f'add list=CN address={net.with_prefixlen} comment="CN MetaCubeX"\n')

    OUT_COUNT.write_text(str(len(networks)) + "\n", encoding="utf-8")
    OUT_SOURCE.write_text(SOURCE_URL + "\n", encoding="utf-8")

    print(f"Generated CN.rsc with {len(networks)} IPv4 CIDR entries")


if __name__ == "__main__":
    main()

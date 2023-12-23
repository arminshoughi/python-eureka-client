import socket, ipaddress
from typing import Tuple
from ifaddr import get_adapters

from py_eureka_client.logger import get_logger

_logger = get_logger("netint_utils")


def get_host_by_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        _logger.warning("Error when getting host by ip", exc_info=True)
        return ip


def get_ip_by_host(host):
    try:
        return socket.gethostbyname(host)
    except:
        _logger.warning("Error when getting ip by host", exc_info=True)
        return host


def get_first_non_loopback_ip(network: str = "") -> str:
    adapters = get_adapters()
    for adapter in adapters:
        for iface in adapter.ips:
            if iface.is_IPv4:
                _ip = iface.ip
                if network:
                    if ipaddress.ip_address(_ip) in ipaddress.ip_network(network):
                        return _ip
                elif _ip != "127.0.0.1":
                    return _ip
    return ""


def get_ip_and_host(network: str = "") -> Tuple[str, str]:
    ip = get_first_non_loopback_ip(network=network)
    host = socket.gethostname() if not ip else get_host_by_ip(ip)
    if not ip:
        ip = socket.gethostbyname(host)
    return ip, host

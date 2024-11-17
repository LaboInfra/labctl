import wgconfig

def generate_config(device: dict, private_key: str, config_file: str):
    wg = wgconfig.WGConfig(config_file)
    wg.add_attr(None, "PrivateKey", private_key)
    wg.add_attr(None, "Address", f"{device['ipv4']}/32, {device['ipv6']}/128")
    wg.add_attr(None, "DNS", ", ".join(device["dns"]))
    wg.add_attr(None, "MTU", device["mtu"])

    wg.add_peer(device["server_public_key"], "# LaboInfra WireGuard Server Client")
    wg.add_attr(device["server_public_key"], "Endpoint", device["endpoint"])
    wg.add_attr(device["server_public_key"], "AllowedIPs", ", ".join(device["allowed_ips"]))
    wg.add_attr(device["server_public_key"], "PersistentKeepalive", device["persistent_keepalive"])
    wg.add_attr(device["server_public_key"], "PresharedKey", device["preshared_key"])

    wg.write_file()

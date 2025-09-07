def is_valid_ip_address(ip_address: str) -> bool:
    values = ip_address.split('.')
    if len(values) != 4:
        return False
    for i in values:
        try:
            if int(i) not in range(256):
                return False
        except ValueError:
            return False
    return True

# Импорт необходимых модулей
import ipaddress  # Для работы с IP-адресами и подсетями
import re         # Для регулярных выражений (в текущей версии не используется, но оставлен для возможного расширения)

def validate_ipv4(ip):
    """
    Проверяет, является ли строка валидным IPv4 адресом.
    Args:
        ip (str): Строка с IP-адресом
    Returns:
        bool: True если адрес валиден, иначе False
    """
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

def validate_ipv6(ip):
    """
    Проверяет, является ли строка валидным IPv6 адресом.
    Args:
        ip (str): Строка с IP-адресом
    Returns:
        bool: True если адрес валиден, иначе False
    """
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ValueError:
        return False

def validate_mask(mask, is_ipv6=False):
    """
    Проверяет корректность маски подсети.
    Args:
        mask (str): Маска в формате CIDR (число) или точечной нотации (для IPv4)
        is_ipv6 (bool): Флаг IPv6 (влияет на максимальное значение маски)
    Returns:
        bool: True если маска валидна, иначе False
    """
    max_mask = 128 if is_ipv6 else 32  # Максимальное значение маски для IPv6/IPv4
    
    # Проверка числового формата CIDR
    if mask.isdigit():
        return 0 <= int(mask) <= max_mask
    
    # Для IPv4 дополнительно проверяем точечную нотацию
    if not is_ipv6:
        try:
            # Преобразуем строку маски в объект IPv4Address для валидации
            ipaddress.IPv4Address(mask)
            return True
        except ValueError:
            return False
    return False

def calculate_network_info(ip_str, mask_str, is_ipv6=False):
    """
    Вычисляет информацию о сети на основе IP и маски.
    Args:
        ip_str (str): IP-адрес в строковом формате
        mask_str (str): Маска подсети
        is_ipv6 (bool): Флаг IPv6
    Returns:
        dict: Словарь с параметрами сети или None при ошибке
    """
    try:
        # Создаем объект сети в зависимости от типа IP
        if is_ipv6:
            ip = ipaddress.IPv6Network(f"{ip_str}/{mask_str}", strict=False)
        else:
            ip = ipaddress.IPv4Network(f"{ip_str}/{mask_str}", strict=False)
        
        # Основные параметры сети
        network = ip.network_address
        # Широковещательный адрес (для IPv6 - последний адрес сети)
        broadcast = ip.broadcast_address if not is_ipv6 else ip.network_address + (ip.num_addresses - 1)
        # Количество доступных адресов (для IPv4 вычитаем 2 - сеть и бродкаст)
        hosts = ip.num_addresses - 2 if not is_ipv6 else ip.num_addresses
        
        # Диапазон доступных хостов
        min_host = network + 1 if not is_ipv6 else network
        max_host = broadcast - 1 if not is_ipv6 else broadcast
        
        # Wildcard маска (инвертированная маска сети)
        wildcard = ip.hostmask
        
        return {
            "network": network,
            "broadcast": broadcast,
            "hosts": hosts,
            "min_host": min_host,
            "max_host": max_host,
            "wildcard": wildcard,
        }
    except ValueError as e:
        print(f"Error: {e}")
        return None

def abbreviate_ipv6(ip_str):
    """
    Сокращает IPv6 адрес согласно стандартному формату.
    Args:
        ip_str (str): IPv6 адрес в строковом формате
    Returns:
        str: Сокращенная форма адреса
    """
    try:
        ip = ipaddress.IPv6Address(ip_str)
        return ip.compressed
    except ValueError:
        return ip_str

def main():
    """
    Основная функция программы - интерфейс взаимодействия с пользователем.
    """
    while True:
        print("\n--- IP Subnet Calculator ---")
        # Выбор режима работы
        mode = input("[1] IPv4 / [2] IPv6 / [q] Quit: ").strip().lower()
        
        # Выход из программы
        if mode == 'q':
            print("Exiting...")
            break
        
        # Проверка корректности выбора режима
        if mode not in ('1', '2'):
            print("Invalid option! Choose 1 (IPv4) or 2 (IPv6).")
            continue
        
        is_ipv6 = mode == '2'  # Флаг IPv6
        
        # Блок ввода IP-адреса с валидацией
        while True:
            ip = input("Enter IP address: ").strip()
            if is_ipv6:
                if validate_ipv6(ip):
                    break
                print("Invalid IPv6 address! Example: 2001:db8::1")
            else:
                if validate_ipv4(ip):
                    break
                print("Invalid IPv4 address! Example: 192.168.1.1")
        
        # Блок ввода маски подсети с валидацией
        while True:
            mask = input("Enter subnet mask (CIDR or dotted format for IPv4): ").strip()
            if validate_mask(mask, is_ipv6):
                break
            print(f"Invalid mask! Must be between 0 and {'128' if is_ipv6 else '32'}.")
        
        # Вычисление параметров сети
        result = calculate_network_info(ip, mask, is_ipv6)
        if not result:
            continue
        
        # Вывод результатов
        print("\n--- Network Summary ---")
        print(f"IP Address: {ip}")
        print(f"Subnet Mask: /{mask}" + (f" (CIDR)" if mask.isdigit() else ""))
        print(f"Network Address: {result['network']}")
        print(f"Wildcard Mask: {result['wildcard']}")
        print(f"Broadcast Address: {result['broadcast']}")
        print(f"Usable Hosts: {result['hosts']:,}")  # Форматирование с разделителями тысяч
        print(f"Host Range: {result['min_host']} - {result['max_host']}")
        
        # Дополнительный вывод для IPv6
        if is_ipv6:
            print(f"Abbreviated IP: {abbreviate_ipv6(ip)}")

if __name__ == "__main__":
    main()

import xmlrpc.client

def set_led_color(num, color, ip="192.168.1.112"):
    with xmlrpc.client.ServerProxy(f"http://{ip}:8000/") as proxy:
        proxy.set_led(num, color)

def clear_all_leds(ip="192.168.1.112"):
    with xmlrpc.client.ServerProxy(f"http://{ip}:8000/") as proxy:
        proxy.clear()
    

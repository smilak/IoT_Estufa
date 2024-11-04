def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid,wifi_pass)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

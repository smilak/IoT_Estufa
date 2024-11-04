def rele():
    while True:
        r=machine.Pin(2, machine.Pin.OUT)
        print(r)
        r.value(1)
        time.sleep(2)
        r.value(0)
        time.sleep(2)

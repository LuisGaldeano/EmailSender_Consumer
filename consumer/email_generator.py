import time

seconds = 0
while True:
    if seconds >= 0:
        print(f"Han pasado {seconds} segundos")
        seconds += 1
        time.sleep(1)

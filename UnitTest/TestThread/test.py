
import threading
import time 

TOTAL = 0
TOTAL_LOCK = threading.Lock()
RESET_TIMER = 10  # Reset timer in seconds

def alert():
    # Define your alert fu
    print("Alert")

def reset_counter():
    global TOTAL
    with TOTAL_LOCK:
        if TOTAL < 1:
            alert()
        TOTAL = 0
    threading.Timer(RESET_TIMER, reset_counter).start()

# Start the initial timer


def main():
    threading.Timer(RESET_TIMER, reset_counter).start()
    global TOTAL
    while True : 
        time.sleep(5)
        TOTAL+= 1
        print(TOTAL)

if __name__ == "__main__": 
    main()
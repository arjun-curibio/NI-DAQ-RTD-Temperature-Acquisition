import threading
import time
import matplotlib.pyplot as plt

def run(stop):
    while True:
        print('thread running')
        time.sleep(1)
        if plt.get_fignums():
            break
                 
def main():
        stop_threads = False
        t1 = threading.Thread(target = run, args =(lambda : stop_threads, ))
        t1.start()
        time.sleep(1)
        stop_threads = True
        t1.join()
        print('thread killed')
main()
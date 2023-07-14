import socket
import json
import time
import sys
import psutil



HOST = '127.0.0.1'
PORT = 1313

if __name__ == '__main__':
    agent_name = sys.argv[1]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except:
            print('connection failed !!!')
            exit()

        while True:
            # metrics
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory()
            cpu_freq = psutil.cpu_freq()[0]

            metrics = {'agent_name': agent_name, 'send_time': time.time(), 'cpu_usage': cpu_usage, 'ram_usage': ram_usage[2], 'cpu_freq': cpu_freq, }
            metrics_json = json.dumps(metrics).encode()

            s.sendall(metrics_json)
            time.sleep(10)
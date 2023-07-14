from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
import time

import asyncio
import json

req_time_list = {}
cpu_usage_list = {}
ram_usage_list = {}

def run_task_req_time(req_time, h: Histogram):
  h.observe(req_time)

def run_task_cpu_usage(cpu_usage, g: Gauge):
  g.set(cpu_usage)

def run_task_ram_usage(ram_usage, g: Gauge):
  g.set(ram_usage)


HOST = '127.0.0.1'
PORT = 1313 # clients port
PORT_P = 8000 # prometheus port

async def task_handler(reader, writer):
  while True:
    metrics_json = await reader.read(1024)
    rcv_time = time.time()
    metrics_json_decoded = metrics_json.decode()
    metrics = json.loads(metrics_json_decoded)
    agent_name = metrics['agent_name']

    if agent_name not in req_time_list:
      x = agent_name + '_req__time'
      y = 'Request time for ' + agent_name
      req_time_list[agent_name] = Histogram(x, y)

    if agent_name not in cpu_usage_list:
      x = agent_name + '_cpu_usage' 
      y  = 'CPU usage for ' + agent_name
      cpu_usage_list[agent_name] = Gauge(x, y)

    if agent_name not in ram_usage_list:
      x = agent_name + '_ram_usage' 
      y  = 'RAM usage for ' + agent_name
      ram_usage_list[agent_name] = Gauge(x, y)

    req_time = rcv_time - metrics['send_time']
    run_task_req_time(req_time, req_time_list[agent_name])
    run_task_cpu_usage(metrics['cpu_usage'], cpu_usage_list[agent_name])
    run_task_ram_usage(metrics['ram_usage'], ram_usage_list[agent_name])


async def main():
    server = await asyncio.start_server(task_handler, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    start_http_server(8000)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        loop.close()

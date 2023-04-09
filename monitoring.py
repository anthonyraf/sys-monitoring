import psutil
import time

class AlertTemplate:
    def __init__(self, resource_name, w_percent, c_percent):
        self.warning_percent = w_percent
        self.critical_percent = c_percent
        self.warning_msg = f"WARNING: The {resource_name} usage has reached {w_percent}%."
        self.critical_msg = f"CRITICAL: The {resource_name} usage has reached {c_percent}%."

    def get_limit(self) -> tuple[int, int]:
        return self.warning_percent, self.critical_percent


class Resource:
    CPU = AlertTemplate("CPU", 70, 85)
    MEMORY = AlertTemplate("Memory", 50, 85)
    DISK = AlertTemplate("Disk", 75, 90)


class PerformanceMonitor:
    def __init__(self):
        self.cpu = psutil.cpu_percent(interval=1)
        self.memory = psutil.virtual_memory().percent
        self.disk = psutil.disk_usage('/').percent
    
    def get_cpu_usage(self):
        return self.cpu

    def get_memory_usage(self):
        return self.memory
    
    def get_disk_usage(self):
        return self.disk


class Handler:
    def __init__(self, resource: Resource, timeout = 1):
        self.cpu = resource.CPU
        self.memory = resource.MEMORY
        self.disk = resource.DISK
        self.timeout = timeout

    def check_cpu_usage(self, monitor):
        cpu_usage = monitor.get_cpu_usage()
        warning_percent, critical_percent = self.cpu.get_limit()
        if cpu_usage >= critical_percent:
            print(self.cpu.critical_msg)
        elif cpu_usage >= warning_percent:
            print(self.cpu.warning_msg)

    def check_memory_usage(self, monitor):
        memory_usage = monitor.get_memory_usage()
        warning_percent, critical_percent = self.memory.get_limit()
        if memory_usage >= critical_percent:
            print(self.memory.critical_msg)
        elif memory_usage >= warning_percent:
            print(self.memory.warning_msg)

    def check_disk_usage(self, monitor):
        disk_usage = monitor.get_disk_usage()
        warning_percent, critical_percent = self.disk.get_limit()
        if disk_usage >= critical_percent:
            print(self.disk.critical_msg)
        elif disk_usage >= warning_percent:
            print(self.disk.warning_msg)
    
    def start(self):
        while True:
            monitor = PerformanceMonitor()

            self.check_cpu_usage(monitor)
            self.check_memory_usage(monitor)
            self.check_disk_usage(monitor)

            time.sleep(self.timeout)



if __name__ == "__main__":
    handler = Handler(Resource, 2)
    handler.start()
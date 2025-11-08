# EdgeQI/Core/scheduler/scheduler.py

import heapq
import time

class Scheduler:
    def __init__(self):
        self.task_queue = []
        self.task_id = 0

    def add_task(self, task_fn, priority=5, task_name="UnnamedTask"):
        """Add a task with priority (lower = higher priority)"""
        self.task_id += 1
        heapq.heappush(self.task_queue, (priority, self.task_id, task_fn, task_name))
        print(f"[Scheduler] Task '{task_name}' added with priority {priority}")

    def run_loop(self, energy_monitor=None, net_monitor=None, mqtt=None):
        """Main loop to process tasks based on priority and system status"""
        print("[Scheduler] Starting task scheduler loop...")
        while True:
            if not self.task_queue:
                print("[Scheduler] No tasks in queue. Sleeping.")
                time.sleep(1)
                continue

            priority, tid, task_fn, task_name = heapq.heappop(self.task_queue)

            # Energy-aware decision
            if energy_monitor and not energy_monitor.is_ok():
                print(f"[Scheduler] Skipping '{task_name}' due to low energy.")
                time.sleep(2)
                continue

            # Network-aware decision
            if net_monitor and not net_monitor.is_ok():
                print(f"[Scheduler] Skipping '{task_name}' due to poor network.")
                time.sleep(2)
                continue

            try:
                print(f"[Scheduler] Executing task: {task_name}")
                result = task_fn()
                if mqtt:
                    mqtt.send_result(task_name, result)
            except Exception as e:
                print(f"[Scheduler] Task '{task_name}' failed: {e}")

            time.sleep(1)  # Delay between tasks
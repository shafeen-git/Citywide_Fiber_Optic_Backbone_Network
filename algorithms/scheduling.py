"""
Algorithm 7: Greedy Activity/Interval Scheduling.
Schedules the maximum number of non-overlapping maintenance intervals.
Complexity: O(M log M) for sorting by earliest finish time, with O(M) linear selection.
"""
from typing import List
from models import MaintenanceTask


def schedule_maintenance_windows(tasks: List[MaintenanceTask]) -> List[MaintenanceTask]:
    sorted_tasks = sorted(tasks, key=lambda t: t.end_hour)
    selected: List[MaintenanceTask] = []
    last_end = -1.0

    for task in sorted_tasks:
        if task.start_hour >= last_end:
            selected.append(task)
            last_end = task.end_hour

    return selected
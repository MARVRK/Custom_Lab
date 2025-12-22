import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable


class State(Enum):
	IN_PROGRESS = auto()
	SLEEP = auto()
	FINISHED = auto()

@dataclass
class Task:
	coroutine : Callable
	state: State

	def step(self):
		new_step = next(self.coroutine)
		if new_step == time.sleep():
			self.state = State.SLEEP

@dataclass
class EventLoop:
	ready_queue = []

	def create_task(self, task: Callable):
		new_task = Task(coroutine=task, state=State.IN_PROGRESS)
		if new_task.state == State.IN_PROGRESS:
			self.ready_queue.append(task)
		raise ValueError("State should start from IN_PROGRESS ")

	def run(self, func: Callable):
		self.create_task(task=func)
		while self.ready_queue is not None:
			for task in self.ready_queue:
				if task.state == State.FINISHED:
					self.ready_queue.pop(task)
				elif task.state == State.IN_PROGRESS:
					Task(coroutine=task).step()
				else:

					continue






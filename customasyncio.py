import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator

class State (Enum):
	IN_PROGRESS = auto ()
	SLEEP = auto ()
	FINISHED = auto ()

@dataclass
class Task:
	coroutine: Generator
	state: State

	def step (self):
		try:
			new_step = next (self.coroutine)
			return new_step
		except StopIteration:
			return State.FINISHED

@dataclass
class EventLoop:
	ready_queue = []
	sleeping_storage = []

	def create_task (self, task: Generator):
		new_task = Task (coroutine=task, state=State.IN_PROGRESS)
		if new_task.state == State.IN_PROGRESS:
			self.ready_queue.append (new_task)
		else:
			raise ValueError ("State should start from IN_PROGRESS ")
		return new_task

	def run (self):
		while self.ready_queue or self.sleeping_storage:
			if len (self.ready_queue) != 0:
				current_task = self.ready_queue.pop (0)
				step = current_task.step ()
				if step == State.FINISHED:
					current_task.state = State.FINISHED
				elif step is None:
					current_task.state = State.IN_PROGRESS
					self.ready_queue.append (current_task)
				elif isinstance (step, int):
					current_task.state = State.SLEEP
					self.sleeping_storage.append ((current_task, step))
			else:
				pass
			new_sleeping = []

			if self.sleeping_storage:
				for task, remaining_ticks in self.sleeping_storage:
					remaining_ticks -= 1
					if remaining_ticks == 0:
						task.state = State.IN_PROGRESS
						self.ready_queue.append (task)
					else:
						new_sleeping.append ((task, remaining_ticks))
			self.sleeping_storage = new_sleeping

def task_A ():
	for x in range (1, 10):
		print (x)
		yield x

def task_B ():
	for x in range (1, 10):
		print (x)
		yield x

if __name__ == "__main__":
		loop = EventLoop()
		loop.create_task (task_A ())
		loop.create_task (task_B ())
		loop.run ()
import time
from enum import Enum, auto
from typing import Generator
from dataclasses import dataclass

class State (Enum):
	FINISHED = auto ()
	IN_PROGRESS = auto ()
	SLEEP = auto ()

@dataclass
class Task:
	coroutine: Generator
	state: State
	sleep_time: int = None

class Sleep:
	def __init__ (self, awaiting_time: int):
		if not isinstance (awaiting_time, int):
			raise ValueError ("Not integer")
		self.awaiting_time = awaiting_time

	def __await__ (self):
		if self.awaiting_time is not None:
			yield self

@dataclass
class Custom_Asyncio:
	ready_queue = []
	sleeping_queue = []

	def gather (self, *args: tuple):
		for task in args:
			self.ready_queue.append (Task (coroutine=task, state=State.IN_PROGRESS))

	def run (self):
		while self.ready_queue or self.sleeping_queue:
			try:
				if len (self.ready_queue) != 0:
					current_task = self.ready_queue.pop (0)
					result = next (current_task.coroutine)
					if isinstance (result, Sleep):
						current_task.state = State.SLEEP
						current_task.sleep_time = time.time() + result.awaiting_time
						self.sleeping_queue.append (current_task)
			except StopIteration:
					current_task.state = State.FINISHED

			time_now = time.time ()
			if self.sleeping_queue:
				for task in self.sleeping_queue:
					if time_now > task.sleep_time:
						self.sleeping_queue.remove(task)
						task.state = State.IN_PROGRESS
						self.ready_queue.append (task)

async def task_A ():
	print ("Task_A Started")
	await Sleep (awaiting_time=2)
	print ("Task_A Continue")
	await Sleep(awaiting_time=2)
	print ("Task_A Finished")

async def task_B ():
	print ("Task_B Started")
	await Sleep (awaiting_time=10)
	print ("Task_B finished")

async def task_C ():
	print ("Task_C Started")
	await Sleep (awaiting_time=4)
	print ("Task_C finished")

if __name__ == "__main__":
	loop = Custom_Asyncio ()
	loop.gather (task_A ().__await__ (), task_B ().__await__ (), task_C ().__await__ ())
	loop.run ()

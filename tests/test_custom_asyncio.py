from customasyncio import EventLoop
from customasyncio import task_B, task_A, State

def test_custom_asyncio ():
	# Given
	loop = EventLoop ()
	# Then
	task1 = loop.create_task (task_B ())
	task2 = loop.create_task (task_A ())
	loop.run ()
	# After
	assert len (loop.ready_queue) == 0
	assert len (loop.sleeping_storage) == 0
	assert task1.state == State.FINISHED
	assert task2.state == State.FINISHED



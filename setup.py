from time import gmtime, strftime, sleep, time
from threading import Timer
import os
import random
from trials import *

# Each process communicates with other processes, and maintains its own logical clock
# Processes are initiated with a speed, and randomly execute actions at regular intervals
# based on their speeds.
class Process:
	def __init__(self, speed, operation_cutoffs, id, log_file_path):
		self.logical_clock = 0
		self.speed = speed
		self.id = id
		self.log_file = open(log_file_path, 'w')
		self.message_queue = []
		self.timer = None
		self.on = True
		self.send_1, self.send_2, self.both_messages = operation_cutoffs
		print("Machine %d initialized with %d operations per second" % (id, speed))

	# Originally, I just had the last line and instead of self.start it was calling self.handle_operation, but it wouldnt repeat the function so I dumped it in here and made it recursive
	def start(self):
		if self.on:
			# Every 1/speed seconds, call handle_operation
			if len(self.message_queue) == 0:
				opcode = random.randint(1,7)
				# Send to to one machine
				if opcode <= self.send_1:
					target_id = (self.id + 1) % 3
					self.send_single_message(target_id)
				# Send to the other machine
				elif opcode <= self.send_2:
					target_id = (self.id - 1) % 3
					self.send_single_message(target_id)
				# Send to both machines
				elif opcode <= self.both_messages:
					target_1 = (self.id + 1) % 3
					target_2 = (self.id - 1) % 3
					self.send_multiple_messages(target_1, target_2)
				# Internal event, update local clock
				else:
					self.internal_event()
			else:
				message = self.message_queue.pop(0)
				self.receive(message)
			self.timer = Timer(1.0/self.speed, self.start).start()

	# Append a message to queue to buffer a received message
	def append_to_message_queue(self, message):
		self.message_queue.append(message)

	# send a message to a single other machine
	def send_single_message(self, target):
		self.logical_clock += 1
		machines[target].append_to_message_queue(self.logical_clock)
		self.log_event("Send to Machine %d" % target)

	# Send a message to both other processes
	def send_multiple_messages(self, target_1, target_2):
		self.logical_clock += 1
		machines[target_1].append_to_message_queue(self.logical_clock)
		machines[target_2].append_to_message_queue(self.logical_clock)
		self.log_event("Send to Both Machines")

	# Increment the logical clock and log the event
	def internal_event(self):
		self.logical_clock += 1
		self.log_event("Internal")

	# Receive a message and update the logical clock accordingly
	def receive(self, timestamp):
		self.logical_clock = max(self.logical_clock, timestamp) + 1
		self.log_event("Receive")

	# Log the event, the system time, and the logical clock time in the log file
	def log_event(self, event):
		# print("Machine Number %d | Logging event: %s | System Time %s | Logical Clock %d" % (self.id, event, strftime("%a, %d %b %Y %H:%M:%S", gmtime()), self.logical_clock))
		self.log_file.write("Logging event: %s | System Time %s | Logical Clock %d \n" % (event, time(), self.logical_clock))

	def stop(self):
		self.on = False


if __name__== "__main__":
	trial = 0
	for speeds in all_speeds:
		for probs in all_probs:
			os.mkdir("trial%d"%trial)
			print("Starting to create machines")
			print("Speeds: " + str(speeds))
			print("Probs: " + str(probs))
			machines = {}
			machines[0] = Process(speeds[0], probs, 0, "trial%d/log_0.log"%trial)
			machines[1] = Process(speeds[1], probs, 1, "trial%d/log_1.log"%trial)
			machines[2] = Process(speeds[2], probs, 2, "trial%d/log_2.log"%trial)

			machines[0].start()
			machines[1].start()
			machines[2].start()

			try:
				# Run for 1 minute
				sleep(60)
				
			finally:
				# Stop them from running
				machines[0].stop()
				machines[1].stop()
				machines[2].stop()
				print("1 minute has elapsed. Logs are generated in trials%d/log_<id>.log"%trial)
				trial += 1
				print("Run plotter separately to see output.")

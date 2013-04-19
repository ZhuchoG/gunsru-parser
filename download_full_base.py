# -*- coding: utf-8 -*-

import imp
import Queue
import threading
#import thread 

parser = imp.load_source('parser', './parser.py')

from parser import *
from redis import Redis
from sets import Set

########################################################################
class SectionDownloader(threading.Thread):
	"""Threaded Section Downloader"""
 
	#----------------------------------------------------------------------
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = sections_queue
 
	#----------------------------------------------------------------------
	def run(self):
		while True:
			# gets the url from the queue
			section = self.queue.get()

			self.download_section(section)

			themes_queue = Queue.Queue()

			for theme in db.smembers("section:"+str(section)):
				theme_id = ast.literal_eval(theme)["id"]

				themes_queue.put([section, theme_id])

			

			for i in range(10):
				t = ThemeDownloader(themes_queue)
				t.setDaemon(True)
				t.start()

			themes_queue.join()

			# send a signal to the queue that the job is done
			self.queue.task_done()
 
	#----------------------------------------------------------------------
	def download_section(self, section):
		""""""
		print "Downloading section " + section + " start"
		parse_section(section)
		print "Downloading section " + section + " end"
 
#----------------------------------------------------------------------

class ThemeDownloader(threading.Thread):
	"""Threaded Section Downloader"""
 
	#----------------------------------------------------------------------
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
 
	#----------------------------------------------------------------------
	def run(self):
		while True:
			# gets the url from the queue
			theme = self.queue.get()

			self.download_theme(theme[0], theme[1])
			
			# send a signal to the queue that the job is done
			self.queue.task_done()
 
	#----------------------------------------------------------------------
	def download_theme(self, section, theme):
		""""""
		print "Downloading theme " + section + "/" + theme + " start"
		parse_theme(section, theme)
		print "Downloading theme " + section + "/" + theme + " end"
 
#----------------------------------------------------------------------

sections_queue = Queue.Queue()


def start_sections_queue(sections):
	
	# create a thread pool and give them a queue
	for i in range(10):
		s = SectionDownloader(sections_queue)
		s.setDaemon(True)
		s.start()

	# wait for the queue to finish
	sections_queue.join()

db = Redis()

# print "Downloading Index start"
# parse_index()
# print "Downloading Index end"

# subindexes = []
# for subindex in db.smembers("index"):
# 	sub_id = ast.literal_eval(subindex)["id"]
# 	print "Downloading subindex " + str(sub_id) + " start"
# 	parse_subindex(sub_id)
# 	subindexes.append(sub_id)
# 	print "Downloading subindex " + str(sub_id) + " end"

subindexes = []
for subindex in db.smembers("index"):
	sub_id = ast.literal_eval(subindex)["id"]
	subindexes.append(sub_id)

sections = Set()
for subindex in subindexes:
	for section in db.smembers("index:"+str(subindex)):
		sect_id = ast.literal_eval(section)["id"]
		sections.add(sect_id)

# give the queue some data
for section in sections:
	sections_queue.put(section)

start_sections_queue(sections)









	








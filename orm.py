import sqlite3


# for item in data_tuple:
# 	event = {}
# 	event['title'] = item[0]
# 	event['description'] = item[1]
# 	event['date'] = item[2]
# 	event['id'] = str(item[3])
# 	events.append(event)

class Event:
	def __init__(self, title, description, date, _id):
		self.title = title
		self.description = description
		self.date = date
		self._id = _id

	def get_dict(self):
		return {
			'title': self.title,
			'description': self.description,
			'date': self.date,
			'id': self._id,
		}

	def get_tuple(self):
		return (self.title, self.description, self.date, self._id)



class Mapper:
	def __init__(self):
		self.con = sqlite3.connect('basic.db')
		self.cur = self.con.cursor()
		# self.events = []
		# self.table_name = 'basic'

	def create_event(self, title, description, date, id):
		# try:
		# validate
		event = Event(title, description, date, id)
		self.cur.execute('INSERT INTO basic VALUES(?, ?, ?, ?)', event.get_tuple())
		# close transaction, and probably save the data to a database
		self.con.commit()
		return event


	def get_events(self):
		res = self.cur.execute('SELECT * FROM basic')
		raw_events_data = res.fetchall()
		events = []
		for data in raw_events_data:
			event = Event(data[0], data[1], data[2], data[3])
			events.append(event)
		return events

	def get_event(self, id):
		res = self.cur.execute('SELECT * FROM basic WHERE id = ?', (id, ))
		raw_event_data = res.fetchone()
		event = Event(raw_event_data[0], raw_event_data[1], raw_event_data[2], raw_event_data[3])
		return event	

mapper = Mapper()

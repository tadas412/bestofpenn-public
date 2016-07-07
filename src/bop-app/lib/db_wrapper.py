import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import MySQLdb

db_info = {
	'identifier' : 'bestofpennmysql',
	'user' : '***',
	'pass' : '***',
	'db' : '***',
	'endpoint' : '***',
	'port' : 3306
}


import re


def verify_email(email):
	if not re.match(r".*@[a-zA-Z]*\.*upenn\.edu", email):
		return False
	return True

# verifies email is from penn, checks user doesn't already exist, adds user to Users
def create_user(email, password):
	email = email.lower()
	if not verify_email(email):
		logger.info("create_user; email verification failed on email " + email)
		return 2
	credit_total = 0
	flag_count = 0
	quality_weight = 1

	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
		if num_rows > 0:
			logger.info("create_user; tried to create duplicate user")
			return 1

		cursor.execute("INSERT INTO users (email, passw, credit_total, flag_count, quality_weight) VALUES(%s, %s, %s, %s, %s);", 
			(email, password, credit_total, flag_count, quality_weight))
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("create_user; MySQL error: " + repr(err))
		return 1
	return 0

def get_user(email):
	user = None
	email = email.lower()
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT user_id, email, passw, credit_total, quality_weight FROM users WHERE email = %s;", (email,))
		if num_rows == 0:
			logger.info("get_user; tried to login as invalid user")
			return None
		result = cursor.fetchone()
		user = {
			'user_id' : int(result[0]),
			'email' : result[1],
			'password' : result[2],
			'credit_total' : int(result[3]),
			'quality_weight' : float(result[4])
		}
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("get_user; MySQL error: " + repr(err))
		return None
	return user

def get_user_credit(email):
	credit_total = None
	email = email.lower()
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT credit_total FROM users WHERE email = %s;", (email,))
		if num_rows == 0:
			logger.info("get_user_credit; tried to login as invalid user")
			return None
		result = cursor.fetchone()
		credit_total = int(result[0])
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("get_user_credit; MySQL error: " + repr(err))
		return None
	return credit_total

def add_user_credit(user_id, num_credit):
	credit_total = None
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT credit_total FROM users WHERE user_id = %s;", (user_id,))
		if num_rows == 0:
			logger.info("get_user_credit; tried to login as invalid user")
			return None
		result = cursor.fetchone()
		credit_total = float(result[0])
		new_credit_total = credit_total + num_credit
		cursor.execute("UPDATE users SET credit_total = %s WHERE user_id = %s", (new_credit_total, user_id))
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("add_user_credit; MySQL error: " + repr(err))
		return None
	return True


def verify_list_name(name):
	return name is not None and name != ""

def create_list(creator_id, name, desc):
	if not verify_list_name(name):
		logger.info("create_list; list name verification failed on list " + name)
		return 1
	flag_count = 0

	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM lists WHERE list_name = %s;", (name,))
		if num_rows > 0:
			logger.info("create_list; tried to create duplicate list")
			return 1

		cursor.execute("INSERT INTO lists (creator_id, list_name, description, flag_count) VALUES(%s, %s, %s, %s);", 
			(creator_id, name, desc, flag_count))
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("create_list; MySQL error: " + repr(err))
		return 1
	return 0

# returns list of dicts with keys of topic id, name, desc
def get_lists():
	lists = []
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		cursor.execute("SELECT l.list_id, l.list_name, l.description, COUNT(r.rating) as ct FROM lists AS l LEFT JOIN entities AS e ON e.list_id = l.list_id LEFT JOIN ratings AS r ON r.entity_id = e.entity_id GROUP BY l.list_id ORDER BY ct DESC;")

		results = cursor.fetchall()
		for res in results:
			list_dict = {
				'topic_id' : int(res[0]),
				'name' : res[1],
				'desc' : res[2],
				'num_ratings' : int(res[3])
			}
			lists.append(list_dict)

		cxn.close()
	except MySQLdb.Error, err:
		logger.info("get_lists; MySQL error: " + repr(err))
		return None
	return lists

# returns a dict with all the attributes
def get_list(list_id):
	result = dict()
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM lists WHERE list_id = %s;", (list_id,))
		if num_rows < 1:
			logger.info("get_list; got invalid list")
			return None

		res = cursor.fetchone()
		result = {
			'list_id' : int(res[0]),
			'creator_id' : int(res[1]),
			'list_name' : res[2],
			'description' : res[3],
			'flag_count' : int(res[4])
		}
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("get_list; MySQL error: " + repr(err))
		return None
	return result

def verify_entity_name(name):
	return name is not None and name != ""

def create_entity(creator_id, list_id, name, desc):
	if not verify_entity_name(name):
		logger.info("create_entity; entity name verification failed on entity " + name)
		return 1
	flag_count = 0
	avg_rating = 0
	
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM entities WHERE entity_name = %s AND list_id = %s;", (name, list_id))
		if num_rows > 0:
			logger.info("create_entity; tried to create duplicate entity")
			return 1

		logger.info("create_entity 3")
		cursor.execute("INSERT INTO entities (creator_id, list_id, entity_name, entity_desc, flag_count, avg_rating) VALUES(%s, %s, %s, %s, %s, %s);", \
			(creator_id, list_id, name, desc, flag_count, avg_rating))
		logger.info("create_entity 4")
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("create_entity; MySQL error: " + repr(err))
		return 1
	return 0

# returns list of dicts with keys of entity id, name, desc, avg_rating
def get_entities(topic_id):
	entities = []
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		cursor.execute("SELECT entity_id, entity_name, entity_desc, avg_rating FROM entities WHERE list_id = %s ORDER BY avg_rating DESC", (topic_id,))

		results = cursor.fetchall()
		for res in results:
			entity_dict = {
				'entity_id' : int(res[0]),
				'name' : res[1],
				'desc' : res[2],
				'avg_rating' : float(res[3])
			}
			entities.append(entity_dict)
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("create_entity; MySQL error: " + repr(err))
		return None
	return entities

# returns list of dicts with keys of entity id, name, desc, avg_rating, user_rating
def get_entities_by_user(topic_id, user_id):
	entities = []
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		cursor.execute("SELECT entity_id, entity_name, entity_desc, avg_rating FROM entities WHERE list_id = %s ORDER BY avg_rating DESC", (topic_id,))
		results = cursor.fetchall()
		


		for res in results:
			cursor.execute("SELECT rating FROM ratings WHERE user_id = %s AND entity_id = %s", (user_id,int(res[0])))
			result = cursor.fetchone()
			user_rating = None if not result else int(result[0])
			entity_dict = {
				'entity_id' : int(res[0]),
				'name' : res[1],
				'desc' : res[2],
				'avg_rating' : float(res[3]),
				'user_rating' : user_rating
			}
			entities.append(entity_dict)
		cxn.close()
	except MySQLdb.Error, err:
		print("create_entity; MySQL error: " + repr(err))
		return None
	return entities

def add_rating(user_id, entity_id, rating):
	#logger.info(str(user_id) + " id added to entity id " + str(entity_id) + " with rating " + str())
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM ratings WHERE user_id = %s AND entity_id = %s;", (user_id, entity_id))
		if num_rows > 0:
			cursor.execute("UPDATE ratings SET rating=%s WHERE user_id=%s AND entity_id=%s;",
				(rating, user_id, entity_id))
		else:
			cursor.execute("INSERT INTO ratings (user_id, entity_id, rating) VALUES(%s, %s, %s);", 
			(user_id, entity_id, rating))
		### AGGREGATION MODULE
		cursor.execute("SELECT quality_weight, rating FROM users AS u, ratings AS r WHERE u.user_id=r.user_id AND entity_id = %s;",
			(entity_id,))
		data = cursor.fetchall()
		weight_total = sum([a[0] for a in data])
		score = 0
		for row in data:
			score += row[1] * (row[0] / weight_total)
		cursor.execute("UPDATE entities SET avg_rating=%s WHERE entity_id=%s;",
				(score, entity_id))
		cxn.commit()
		cxn.close()
		logger.info("rating added")
	except MySQLdb.Error, err:
		logger.info("add_rating; MySQL error: " + repr(err))
		return 1
	return 0

# returns an int if the user has already rated the entity, None otherwise
def get_rating(user_id, entity_id):
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT rating FROM ratings WHERE user_id = %s AND entity_id = %s;", (user_id, entity_id))
		if num_rows == 0:
			return None
		else:
			return int(cursor.fetchone()[0])
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("get_rating; MySQL error: " + repr(err))
		return None


def add_flag_to_list(user_id, list_id):
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()

		num_rows = cursor.execute("SELECT * FROM list_flags WHERE user_id = %s AND list_id = %s;", (user_id, list_id))
		if num_rows > 0:
			cursor.execute("DELETE FROM list_flags WHERE user_id=%s AND list_id=%s;",
				(user_id, list_id))
		else:
			cursor.execute("INSERT INTO list_flags (user_id, list_id) VALUES(%s, %s);",
				(user_id, list_id))
			cursor.execute("SELECT flag_count FROM lists WHERE list_id=%s;",
				(list_id,))
			result = cursor.fetchone()
			count = result[0] + 1
			if count > 9:
				cursor.execute("DELETE FROM entity_flags WHERE entity_id IN (SELECT entity_id FROM Entities WHERE list_id=%s);", (list_id,))
				cursor.execute("DELETE FROM list_flags WHERE list_id = %s", (list_id,))
				cursor.execute("DELETE FROM ratings WHERE entity_id = %s IN (SELECT entity_id FROM Entities WHERE list_id=%s)", (list_id,))
				cursor.execute("DELETE FROM entities WHERE list_id = %s", (list_id,))
				cursor.execute("DELETE FROM lists WHERE list_id = %s", (list_id,))
			else:
				cursor.execute("UPDATE lists SET flag_count=%s WHERE list_id=%s",
					(count, list_id))
		cursor.execute("SELECT u.flag_count, quality_weight, u.user_id FROM users as u, lists as l WHERE creator_id=user_id AND list_id = %s;", (list_id,))
		result = cursor.fetchone()
		### QC MODULE
		flag_count = result[0] + 1
		quality_weight = result[1] * 0.9
		creator_id = result[2]
		cursor.execute("UPDATE users SET flag_count=%s, quality_weight=%s WHERE user_id=%s", (flag_count, quality_weight, creator_id))
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("add_flag_to_list; MySQL error: " + repr(err))
		return 1
	return 0


def add_flag_to_entity(user_id, entity_id):
	try:
		cxn = MySQLdb.connect(host=db_info['endpoint'], port=db_info['port'], user=db_info['user'], passwd=db_info['pass'], db=db_info['db'])
		cursor = cxn.cursor()
		num_rows = cursor.execute("SELECT * FROM entity_flags WHERE user_id = %s AND entity_id = %s;", (user_id, entity_id))
		if num_rows > 0:
			cursor.execute("DELETE FROM entity_flags WHERE user_id=%s AND entity_id=%s;",
				(user_id, entity_id))
		else:
			cursor.execute("INSERT INTO entity_flags (user_id, entity_id) VALUES(%s, %s);",
				(user_id, entity_id))
			cursor.execute("SELECT flag_count FROM entities WHERE entity_id=%s;",
				(entity_id,))
			result = cursor.fetchone()
			count = result[0] + 1
			if count > 9:
				cursor.execute("DELETE FROM entity_flags WHERE entity_id = %s", (entity_id,))
				cursor.execute("DELETE FROM ratings WHERE entity_id = %s ", (entity_id,))
				cursor.execute("DELETE FROM entities WHERE entity_id = %s", (entity_id,))
			else:
				cursor.execute("UPDATE entities SET flag_count=%s WHERE entity_id=%s",
					(count, entity_id))
		cursor.execute("SELECT u.flag_count, quality_weight, u.user_id FROM users as u, entities as e WHERE creator_id=user_id AND entity_id = %s;", (entity_id,))
		result = cursor.fetchone()
		### QC MODULE
		flag_count = result[0] + 1
		quality_weight = result[1] * 0.9
		creator_id = result[2]
		cursor.execute("UPDATE users SET flag_count=%s, quality_weight=%s WHERE user_id=%s", (flag_count, quality_weight, creator_id))
		cxn.commit()
		cxn.close()
	except MySQLdb.Error, err:
		logger.info("add_flag_to_entity; MySQL error: " + repr(err))
		return 1
	return 0

if __name__ == "__main__":
	logger.info("Main started")



import sys
import csv
import matplotlib.pyplot as plot
import numpy

userFile = sys.argv[1]
entityFile = sys.argv[2]
listsFile = sys.argv[3]
ratingsFile = sys.argv[4]

users = {}

with open(userFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        userID = row[0]
        users[userID] = {}

with open(entityFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        userID = row[0]
        numEntities = int(row[1])
        users[userID]["num_entities_created"] = numEntities

with open(listsFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        userID = row[0]
        numLists = int(row[1])
        users[userID]["num_lists_created"] = numLists

with open(ratingsFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        userID = row[0]
        numRatings = int(row[1])
        users[userID]["num_ratings"] = numRatings

for u in users:
    vals = users[u]
    if "num_entities_created" not in vals:
        users[u]["num_entities_created"] = 0
    if "num_lists_created" not in vals:
        users[u]["num_lists_created"] = 0
    if "num_ratings" not in vals:
        users[u]["num_ratings"] = 0

print "\n\nnum_entities_created, num_ratings"
for u in users:
    val = users[u]
    print "[{}, {}],".format(val["num_entities_created"], val["num_ratings"])

print "\n\nnum_lists_created, num_ratings"
for u in users:
    val = users[u]
    print "[{}, {}],".format(val["num_lists_created"], val["num_ratings"])

print "\n\nnum_lists_created, num_entities_created"
for u in users:
    val = users[u]
    print "[{}, {}],".format(val["num_lists_created"], val["num_entities_created"])

ratings = [users[u]["num_ratings"] for u in users]
lists = [users[u]["num_lists_created"] for u in users]
entities = [users[u]["num_entities_created"] for u in users]

print "avg number of ratings: {}".format(numpy.mean(ratings))
print "avg number of lists created: {}".format(numpy.mean(lists))
print "avg number of entities created: {}".format(numpy.mean(entities))




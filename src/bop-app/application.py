# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, json, flash
from werkzeug import generate_password_hash, check_password_hash
import datetime
import random
import uuid
import smtplib
import os
from lib import db_wrapper
import logging
#import sys  

#reload(sys)  
#sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# create the application object
application = Flask(__name__)
application.secret_key = 'bestofpenn-secret'
application.config['UPLOAD_FOLDER'] = 'static/uploads'

@application.route('/')
def main():
    if session.get('user'):
        return redirect('/homePage')
    else:
        return redirect('/showSignin')


@application.route('/showSignUp')
def showSignUp():
    flash(u'Signing up placeholder!')
    return render_template('signup.html')

@application.route('/message/<message_text>')
def error(message_text):
    return render_template('error.html', error=message_text)

@application.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        user_in_db = db_wrapper.get_user(_email)
        if user_in_db:

            return json.dumps({'error':'user already exists'})

        # validate the received values
        if _email and _password:
            # add to db
            res = db_wrapper.create_user(_email, generate_password_hash(_password))
            logger.info("rest = " + str(res))
            if res == 0:
                return json.dumps({'error':('user ' + _email + " created successfully")})
            return json.dumps({'error': (_email + " is not a Penn email")})

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})


@application.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@application.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
 
        #user = dynamo.admin.get_item(email=_email)
        user = db_wrapper.get_user(_email)
        if not user:
            render_template('error.html',error = "User doesn't exist!")
            return redirect('/showSignin')

        if check_password_hash(user['password'], _password):
            session['user'] = user['email']
            session['userID'] = user['user_id']
            return redirect('/homePage')
    
        else:
            return render_template('error.html',error = 'Wrong Password!')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))


@application.route('/homePage')
def homePage():
    if session.get('user'):
        return render_template('homePage.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@application.route('/clearTopic')
def clearTopic():
    session.pop('topicID',None)
    return redirect('/homePage')

@application.route('/logout')
def logout():
    session.pop('user',None)
    session.pop('topicID',None)
    return redirect('/')

@application.route('/showAddTopic')
def showAddTopic():
    return render_template('addTopic.html')

@application.route('/showAddEntity')
def ShowAddEntity():
    return render_template('addEntity.html')

@application.route('/addTopic',methods=['POST'])
def addTopic():
    try:
        if session.get('user'):
            _name = request.form['inputName']
            _description = request.form['inputDescription']
            _userID = session.get('userID')
            _filePath = ''
            if request.form.get('filePath') is not None:
                _filePath = request.form.get('filePath')

            _description = _description + "_PIC:" + _filePath
            
            db_wrapper.create_list(_userID, _name, _description)

            return redirect('/homePage')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = "This topic name already exists!")


@application.route('/addEntity',methods=['POST'])
def addEntity():
    try:
        if session.get('user') and session.get('topicID'):
            _name = request.form['inputName']
            _description = request.form['inputDescription']
            _userID = session.get('userID')
            _listID = session.get('topicID')
          
            db_wrapper.create_entity(_userID, _listID, _name, _description)
            return redirect('/getTopicHome')
    
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = "This topic name already exists! " + repr(e))

@application.route('/getTopic')
def getTopic():
    try:
        if session.get('user'):
            # get input
            _email = session.get('user')
            _name = session.get('name')
            _credits = db_wrapper.get_user_credit(_email)

            topics = db_wrapper.get_lists()
            # grab topics
            #topics = dynamo.admin_topic.scan(admin_email__eq=_email)

            # place each topic in json format
            topics_dict = []
            for topic in topics:
                all_desc = topic['desc']
                description = all_desc
                filepath = 'http://placehold.it/150x150'
                if '_PIC:' in all_desc:
                    description = all_desc.split('_PIC:')[0]
                    filepath = all_desc.split('_PIC:')[1]

                topic_dict = {
                    'ID': topic['topic_id'],
                    'Name': topic['name'],
                    'Description': description,
                    'FilePath': filepath,
                    'Credits': _credits,
                    'Ratings': topic['num_ratings']
                }

                topics_dict.append(topic_dict)
            return json.dumps(topics_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@application.route('/setTopic',methods=['POST'])
def setTopic():
    try:        
        _topicID = request.form['topicID']

        session['topicID'] = _topicID

        return redirect('/getTopicHome')

    except Exception as e:
        return render_template('error.html',error = str(e))


@application.route('/getTopicHome')
def getTopicHome():
    if session.get('topicID'):
        _topicID = session.get('topicID')
        entities = db_wrapper.get_entities(_topicID)
        relevant_topic = db_wrapper.get_list(_topicID)
        #entities = dynamo.users.scan(topic_name__eq=_topic)
        count = 0
        for entity in entities:
            count += 1

        return render_template('topicHome.html',topic_name=relevant_topic['list_name'],size=count)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@application.route('/getTopicEntities')
def getTopicEntities():
    try:
        if session.get('topicID'):
            _topicID = session.get('topicID')
            _userid = session['userID']

            entities = db_wrapper.get_entities_by_user(_topicID,_userid)

            # place each entity in json format
            entities_dict = []
            for entity in entities:
                rating = "{0:.2f}".format(entity['avg_rating'])
                user_rating = 'None'
                if entity['user_rating']:
                    user_rating = str(entity['user_rating']) + " stars"

                mem_dict = {  
                    'ID' : entity['entity_id'],  
                    'Name': entity['name'].decode('latin-1').encode('utf-8'),
                    'Desc': entity['desc'].decode('latin-1').encode('utf-8'),
                    'Rating':rating,
                    'UserRating':user_rating
                }
                entities_dict.append(mem_dict)

            print entities_dict
            return json.dumps(entities_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        print "exception! " + repr(e)
        return render_template('error.html', error = str(e))

@application.route('/addEntityRating',methods=['POST'])
def addEntityRating():
    try:
        if session.get('topicID'):
            _userID = session['userID']
            # print(_userID)
            # print(session)
            # print(session['userID'])
            _topicID = session.get('topicID')
            # print request.form
            _entityID = int(request.form['entityID'])
            _rating = int(request.form['rating'])
            print (_userID,_entityID, _rating)
            # print(_userID + ", entity_ID: " + _entityID + " | rating: " + _rating)

            db_wrapper.add_rating(_userID, _entityID, _rating)
            db_wrapper.add_user_credit(_userID, 0.5)
            print("did add rating")
         
    except Exception as e:
        return render_template('error.html', error = str(e))
    return redirect('/getTopicHome')

@application.route('/addEntityFlag',methods=['POST'])
def addEntityFlag():
    logger.info("adding entity flag")
    try:
        if session.get('topicID'):
            _userID = session['userID']

            _topicID = session.get('topicID')
            _entityID = int(request.form['entityID'])

            db_wrapper.add_flag_to_entity(_userID, _entityID)
            print("did add flag to entity")
         
    except Exception as e:
        return render_template('error.html', error = str(e))
    return redirect('/getTopicHome')

@application.route('/addListFlag',methods=['POST'])
def addListFlag():
    try:
        if session.get('userID'):
            _userID = session['userID']

            _topicID = request.form['topicID']

            print (_userID,_topicID)

            db_wrapper.add_flag_to_list(_userID, _topicID)
            print("did add flag to list")
         
    except Exception as e:
        return render_template('error.html', error = str(e))
    return redirect('/homePage')

@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})

if __name__ == "__main__":
    application.run()
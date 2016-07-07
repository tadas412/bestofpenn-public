<h1>Overview</h1>

Description: Crowdsourcing Penn student knowledge to determine the best locales for various activities in the Philadelphia area.

Problem Solved: It takes the typical Penn student years of experience to understand how to make the most of their Penn experience on a week by week basis. Where should I take my parents out to dinner while they’re visiting? What are the best BYO’s? What are the prime study spots on campus? The Best of Penn app consolidates all that information in a digital, reviewable, and accurate format. 

<h3>User Flow</h3>

Our web application has all of its members act as both contributors and users. Only people with an @*.upenn.edu email address can be part of the site. Upon visiting the home page, users will be prompted to log in.

Upon logging in, they have two options: view a “Best of” List, or contribute a new list. If they choose to contribute a new list, they are taken to a separate UI view where they enter a list name, description, and 3 entity options. 

If they instead choose to view an existing list, they will be be presented with a UI view that shows the existing list’s entities. If they think the list is inappropriate for Best of Penn, they can flag it. They can rate (1-5) each existing entity within the list, they can flag an entity that they think is irrelevant or duplicate to the list, and they can choose to add a new entity to the list.

<h3>Incentive & Quality Control System</h3>

Every user will be associated with a profile that has a particular number of “credits.” Every user starts with 10 credits. At all times, you can view the 5 most popular (i.e. with most votes) lists for no credit. 
<ul>
<li>+0.5 credit for every entity to which you add a rank</li>
<li>+2 credit if your submitted entity gets rank 4+</li>
<li>+2 credit if your submitted list gets 20+ views</li>
<li>-1 credit if your submitted entity gets 5+ flags</li>
<li>-1 credit if your submitted list gets 5+ flags</li>
<li>-2 credit for unlocking another list to view</li>
</ul>

<h3>Quality Control and Aggregation Module</h3>

For the quality control module, we have created a field for each user that keeps track of their quality_weight. This field is initiated for every new user to be equal to 1.0. Every time an entry/list that a user created is flagged by another user (where flagging corresponds to inappropriate, fake or irrelevant content), we decrease that users quality weight by 10%. For instance, if a user has 3 flagged entries, their quality weight score is lowered to 1 * 0.9^3 = .729.

We then use this property of each user to in the aggregation module. We decided not to count each user’s input and rating equally, but instead calculated an entity’s average rating based on a weighted rating along with the users’ quality_weights. If a user does not get any flagged entries and has a high quality_weight, their rating should be weighted higher than the ratings of a user who is constantly flagged for content they post. Therefore, when aggregating the data of the ratings for a particular list, we have a formula for calculating an entity’s rating: sum of all users [ (user's quality rating / sum of all quality ratings relevant to the entity) * user's rating ]. Once the ratings are calculated for each entry in a specific list, they are listed in the UI in order of rating, with the highest rated place/entry listed first. We also decided to have the ratings be only from 1-5 where 5 stars corresponds to the best and 1 star is the worst.

In regards to Deliverable 2...

The code for the quality control and aggregation modules is integrated into db_wrapper.py, and pseudocode can be found in the control_module.py file. 

Sample input/output data, as well as raw data for tha application in general, can be found in .xlsx format under the data/ directory. DBSchema.docx shows how we have this stored in an Amazon RDS MySQL database (which is already live).

We still need to write code for the proposed incentive credit system and integrate that into our DB schema. Besides that, the majority of our work will involve creating and deploying a web interface to utilize this backend.
 

<h3>Components to Implement</h3>

<b>Web Application (17)</b>
<ol>
	<li>User Interface (12)</li>
	<ul>
		<li>Login page (1)</li>
		<li>Account creation page (1)</li>
		<li>Homepage (2)</li>
		<li>List creation page (1)</li>
		<li>Entity list (3)</li>
		<li>Integration of credit system (4)</li>
	</ul>
	<li>Database (5)</li>
	<ul>
		<li>Defining schema (1)</li>
		<li>DB setup (1)</li>
		<li>DB wrapper methods for client interaction (3)</li>
	</ul>
</ol>
<br>
<b>Aggregation Module (1)</b>
<ol>
	<li>Rating aggregation (1)</li>
	<ul>
		<li>Compute ratings based on rating by user</li>
		<li>Use a higher weight for the ratings performed by high quality users</li>
	</ul>
</ol>
<br>
<b>Quality Module (5)</b>
<ol>
	<li>Account creation verification (1)</li>
	<ul>
		<li>Verify email entered is a valid email and upenn.edu email</li>
		<li>Check whether account creation is not genuine (with IP address request frequency)</li>
	</ul>
	<li>Account update verification (1)</li>
	<ul>
		<li>Remove users with number of flagged suggestions beyond a threshold</li>
	</ul>
	<li>Account quality rating (1)</li>
	<ul>
		<li>Compute credit & quality of each worker based</li>
	</ul>
	<li>List creation & Entity creation verification (1)</li>
	<ul>
		<li>Check that lists of entities are not duplicated</li>
		<li>Check syntax of list and entity names</li>
	</ul>
	<li>Rating entered verification (1)</li>
	<ul>
		<li>Check whether rating was previously entered by the user, if so update the rating rather than add a new rating</li>
	</ul>



<h3>Part 3 Code Explanation</h3>

The web application is built using Python Flask. All code used for the prototype is in /src.

<h4>Dependencies</h4>

Dependencies for the application are installed into the virtual environment, which is 
saved in /src/bop-venv.

<h4>Database</h4>
Scripts for setting up the MySQL database and adding fake data can be found
in /src/db_setup. The MySQL database is hosted on AWS Relational Database Service (RDS).

The database wrapper, src/bop-app/lib/db_wrapper.py,
handles interaction with the database. All the SQL queries are contained in this wrapper.
It also handles validation of emails
during user registration, by checking that that is matches the pattern *@*.upenn.edu.
This is part of the quality module, by requiring that users be affiliated 
with Penn. The wrapper also handles aggregation of the data that is entered by users. For example, ratings for a particular entity are averaged before being displayed.

<h4>Web Application</h4>
The web application logic is contained in src/bop-app/application.py.
It contains configuration for all the routes for the application, and the functionality
for each route. 

Static files such as CSS, images or JS scripts are placed in /src/bop-app/static. 

Templates used for generating HTML pages are placed in /src/bop-app/templates. Contents of templates can be dynamically generated. For example, if there is a list of entities that belong to a particular topic, the list of entities can be placed into a table in the final HTML page.

The details for each route are as follows:
<ul>
	<li>/: Routes to /homePage if session has username, to /showSignin in there is no user logged in</li>
	<li>/showSignUp: displays the user registration page</li>
	<li>/message: an internal route that displays the specified error message</li>
	<li>/signUp: a POST request to this route creates a user. Validation is also performed before a user is created</li>
	<li>/showSignin: login page</li>
	<li>/validateLogin: a POST request validates the email and password entered by the user. If login information is correct, the user is redirected to the home page</li>
	<li>/homePage: displays a list of the topics available</li>
	<li>/clearTopic: clears the current topicID stored in the session</li>
	<li>/logout: removes the user information from the session</li>
	<li>/showAddTopic: displays options for user to enter a new topic</li>
	<li>/showAddEntity: displays options for user to enter a new entity, or item in a topic</li>
	<li>/addTopic: adds specified topic to the databse</li>
	<li>/addEntity: adds specified entity to the database</li>
	<li>/getTopic: returns list of topics that are available, along with its relevant information</li>
	<li>/setTopic: sets current topicID into the session</li>
	<li>/getTopicHome: displays entities of a particular topic. The user can add a rating to each entity in the topic</li>
	<li>/getTopicEntities: returns a list of the entities that belong to a topic</li>
	<li>/addEntityRating: adds rating for a particular entity. A user is only allows one rating per entity</li>
	<li>/addEntityFlag: adds a flag to a particular entity. A flag indicates the poor quality of an entity suggestion.</li>
	<li>/addListFlag: adds a flag to a particular topic.</li>
</ul>













# Best of Penn
#####NETS 213 Final Project Spring 2016
Bianca Pham, Nathaniel Chan, Steffi Maiman, Stephanie Hsu, Tadas Antanavicius

##Overview

Description: Crowdsourcing Penn student knowledge to determine the best locales for various activities in the Philadelphia area.

Problem Solved: It takes the typical Penn student years of experience to understand how to make the most of their Penn experience on a week by week basis. Where should I take my parents out to dinner while they’re visiting? What are the best BYO’s? What are the prime study spots on campus? The Best of Penn app consolidates all that information in a digital, reviewable, and accurate format. 

##User Flow


Our web application has all of its members act as both contributors and users. Only people with an @*.upenn.edu email address can be part of the site. Upon visiting the home page, users will be prompted to log in.

Upon logging in, they have two options: view a “Best of” List, or contribute a new list. If they choose to contribute a new list, they are taken to a separate UI view where they enter a list name, description, and 3 entity options. 

If they instead choose to view an existing list, they will be be presented with a UI view that shows the existing list’s entities. If they think the list is inappropriate for Best of Penn, they can flag it. They can rate (1-5) each existing entity within the list, they can flag an entity that they think is irrelevant or duplicate to the list, and they can choose to add a new entity to the list.

##Incentive & Quality Control System

Every user will be associated with a profile that has a particular number of “credits.” Every user starts with 10 credits. At all times, you can view the 5 most popular (i.e. with most votes) lists for no credit. 

+0.5 credit for every entity to which you add a rank
+2 credit if your submitted entity gets rank 4+
+2 credit if your submitted list gets 20+ views
-1 credit if your submitted entity gets 5+ flags
-1 credit if your submitted list gets 5+ flags
-2 credit for unlocking another list to view


##Components to Implement

#####Web Application (17)
- User Interface (12)
  - Login page (1)
  - Account creation page (1)
  - Homepage (2)
  - List creation page (1)
  - Entity list (3)
  - Integration of credit system (4)
- Database (5)
  - Defining schema (1)
  - DB setup (1)
  - DB wrapper methods for client interaction (3)

#####Aggregation Module (1)
- Rating aggregation (1)
	- Compute ratings based on rating by user
	- Use a higher weight for the ratings performed by high quality users

#####Quality Module (5)
- Account creation verification (1)
	- Verify email entered is a valid email and upenn.edu email
	- Check whether account creation is not genuine (with IP address request frequency)
- Account update verification (1)
	- Remove users with number of flagged suggestions beyond a threshold
- Account quality rating (1)
	- Compute credit & quality of each worker based
	- List creation & Entity creation verification (1)
	- Check that lists of entities are not duplicated
	- Check syntax of list and entity names
- Rating entered verification (1)
	- Check whether rating was previously entered by the user, if so update the rating rather than add a new rating

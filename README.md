group-22-2013
=============
Project Plan
------------

Goals and objectives
--------------------

	The aim of this project is to create an online version of an old-fashioned photo album. In the service, 
	a user can create photo albums, share them, and each user with a shared  copy can place orders to get 
	printed copies of albums.
	
Tools and frameworks
--------------------

* Eclipse IDE
* PyDev package
* Django framework
* PostgreSQL
* GitHub
	
Functionalities
---------------

    
* Authentication

  > Using Django's session framework
   
* Basic album functionalities

  > Using CSS for the layouts and styles
  
* Public link to photo albums

  > generate a unique url for every album and set private/public attribute for the albums
  
* Share albums

  > Using Facebook share
  
* Order albums

  > Using the simple payment site
  
* Integrate with an image service API

  > Integrate with Flickr
  
* 3rd party login

  > Implementing Facebook login
  
  
* Use of Ajax
	
Timeline
--------

	The project will be divided into 6 sprints, one sprint for a week, starting from the 6th of January.
	
Tasks for the first week
------------------------

	Implement the Django models
	Create the structure of the project and website

Tasks for the second week
-------------------------

	Authentication - on the server side
	3rd party login
	Create the templates for the views
	
Tasks for the third week
------------------------

	Create the basic functionalities - both on the client and server side
		
Tasks for the fourth week
-------------------------

	Tasks are divided between the members of the team
		Creating public links - client side
		Sharing albums - client side
		Integration with Flickr - client side
	
Tasks for the fifth week
------------------------

	Implementing the ordering functionality - client side
	Payment functionality - server side
	
Task for the sixth week
-----------------------

	Testing and finalizing the project

Project structure
-----------------

### Models
* User - Django.auth
* Album

  > Title
  
  > Date
  
  > Link
  
  > Status (public or private)

  > Owner (Foreign key to User)
  
* Page
			
  > Layout

  > Containing Album (Foreign key to Album)
		
* Picture

  > Title
  
  > Source
  
  > Containing Page (Foreign key to Page)
  
* Payments

  > PID
  
  > Date
  
  > Reference
  
  > Amount
  
  > Item (Foreign key to Album)
  
  > Buyer (Foreign key to User)
  
### Views

	Handle interactions between templates and the models.
	
### Templates

* Main page

  > Welcome!
  
  > See featured albums
  
  > Authentication (Register / login)
  
* Home page

  > Create albums
  
  > Delete existing albums
  
  > View existing albums
  
* Profile page

  > User settings - for example changing passwords etc.
  
  > View orders
  
* Explore page

  > Browse other people's public albums

* View page  

  > View selected album
  
  > Ability to order albums
  
  > Share album to social media

* Album creating page

  > Select a layout for page
			
  > Set photo urls and captions
  
  > Manage sharing settings (public/private)
  
* Payment page

  > Order overview
  
  > Implement Simple Payment

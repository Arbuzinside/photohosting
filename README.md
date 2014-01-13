group-22-2013
=============
Project Plan

Goals and objectives:
	The aim of this project is to create an online version of an old-fashioned photo album.
	In the service, a user can create photo albums, share them, and each user with a shared copy can place orders to get printed copies of albums.
	
Tools and frameworks:
	Eclipse IDE
	PyDev package
	Django framework
	PostgreSQL
	GitHub
	
Functionalities:
	Authentication
	Basic album functionalities
	Public link to photo albums
	Share albums
	Order albums
	Integrate with an image service API
	3rd party login
	Use of Ajax
	
Timeline:
	The project will be divided into 6 sprints, one sprint for a week, starting from the 6th of January.
	
	Tasks for the first week:
		Implement the Django models
		Create the structure of the project and website
	
	Tasks for the second week:
		Authentication - on the server side
			Using Django's session framework
		3rd party login
			Using existing APIs
		Create the templates for the views
		
	Tasks for the third week:
		Create the basic functionalities - both on the client and server side
			Using AJAX to display images
			Using CSS for the layouts and styles
	
	Tasks for the fourth week:
		Tasks are divided between the members of the team
			Creating public links - client side
			Sharing albums - client side
			Integration with Flickr - client side
		
	Tasks for the fifth week:
		Implementing the ordering functionality - client side
		Payment functionality - server side
		
	Task for the sixth week:
		Testing and finalizing the project

Project structure:
	Models
		Django.auth - User
		Album
			Name
			Date of creation
			Link
			Status (public or private)
			Foreign key to User
		Page
			Layout
			Foreign key to Album
		Picture
			Name
			Source
			Order
			Foreign key to Page
		Payments
			PID
			SID
			Amount
			Foreign key to Album
	Views
		Functions to fill templates with information from the models
	Templates
		Main page
			Welcome!
			See featured albums
		Authentication page
			Register / login
			3rd party login integration
		Profile page
			User settings - for example changing passwords etc.
			View existing albums
		Navigation page
			Create albums
			Delete existing albums
			Browse other people's albums
				Ability to order albums
		Album creating page
			Select a layout
			Upload photos
			Organize pictures
			Manage sharing settings
				Links
				Social media
		Payment page
			Order overview
			Implement Simple Payment - on server side
# heroku-django

https://bid-app-project.herokuapp.com/

***Deployment instructions are in 'deployment.txt' file*****

This project is combination of django_bid_app(rest api)
and angular-bid-app(frontend) : https://github.com/sunilpie1997/angular-bid-app
      
      
This project has been deployed on HEROKU : a cloud platform of SALESFORCE

uploading to amazon-s3:https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html#working-with-static-and-media-assets

a. Database used is Heroku Postgres: an addon which Heroku provides.
b. I have exported my local database 'bid-app' to heroku postgres --->instruction are in 'deployment.txt'.
c.  Requirements file 'requirements.txt' and runtime file 'runtime.txt'(optional) are necessary as 
    these help heroku in detecting if it is a python app.

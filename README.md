# Salmanac

https://rocky-brushlands-52104.herokuapp.com 

Collects users favourite music artists names and scrap music websites to find album release dates. 
Technologies: Django, PostreSQL. Dockerized and deployed on heroku. 

This application hepled me understand topics related to software delpoyment and containers.

This application contains:
- views responsible for login/register/logout actions    
- views which perform web scrapping on music websites and store all data
- views which perform searching for provided artists inside scrapped data 
    and assigns found album release dates to the users.
- views responsible for displaying all collected information
- views used for managing artists and albums
- HTML templates
- admin page

For a frontend I used Bootstrap 4 with customized css attributes.

I am testing and planning to implement:
- Celery scheduled jobs for:
    - executing web scrapping views
    - sending notifications to the users if th app found an album
- REST API to provide stored data outside
- frontend updates
    
    
reuters.py scrapes the website http://feeds.reuters.com/reuters/topNews for URLs, titles, short descriptions, datetimes and records this data in PostgreSQL and MongoDB databases.

reuters.py was written using Python 3 using the following libraries: requests, selenium, psycopg2. Selenium uses the Chrome webdriver, which can be obtained here: https://chromedriver.chromium.org/downloads - make sure you have Chrome (or Chromium) installed with the same version as the webdriver (I am using version 80).

reuters.py makes a connection to a local PostgreSQL database named reuters_db using the credential: username - reuters_user, password - reuters_password.

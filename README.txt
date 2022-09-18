Using the Covid19API - Founder Therapy Task.

* Make sure to run "pip install -r requirements.txt" to get all the necessary packages installed.

1. Create an account using create superuser in the terminal, this will generate a token for you, use it as an authorization in your requests.

2. Through the django admin page press the "+ Add Countries" to fill the database with countries.

3. You can go to /api/v1/subscribe/<str:slug> to add a country to your subscription list, examples of a slug: "south-africa", "palestine", "ukraine", you must have your token in your header.

4. You can view the details for all the users' subscribed countries and then register that information in the database by running the "showcases" command.

5. You can view the top # of countries with a specific case using api/v1/top/<str:case>/<int:number> where case is ("confirmed", "deaths") and number is up to you and optional, default is 3, you must have your token in your header.

6. You can view the top # of countries from a specific date, to another specific date with a specific case using api/v1/topdate/<str:from>/<str:to>/<str:case>/<int:number> where the date format is: YYYY-MM-DD and the cases are:
("confirmed", "recovered", "deaths"), and the number is up to you and optional, default is 3, you also need your token in your header.

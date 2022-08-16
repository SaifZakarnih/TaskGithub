Using the Covid19API - Founder Therapy Task.

1. Create an account using create superuser in the terminal, this will generate a token for you, use it as an authorization in your requests.

2. Before you start, create an admin account and press the " + Add Countries" as an admin in the django admin page.

3. You can go to /api/v1/subscribe/<str:slug> to add a country to your subscription list, examples of a slug: "south-africa", "palestine", "ukraine".

4. You can view the details for all the users' subscribed countries and then register that information in the database by running the "showcases" command.

5. You can view the top # of countries with a specific case using /api/v1/top/<int:number>/<str:case> where case is ("confirmed", "deaths") and number is up to you.

6. You can view the top # of countries from a specific date, to another specific date with a specific case using /api/v1/topbydate/<str:from>/<str:to>/<str:case>/<int:number> where the date format is: YYYY-MM-DD and the cases are:
("confirmed", "recovered", "deaths"), and the number is up to you.
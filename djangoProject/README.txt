Using the Covid19API - Founder Therapy Task.


1. Register an account using /api/regster/, you must provide a (username), a (password) and an (email).

2. You can use the token provided to you as a response after registering, or you can login through /api/login/ with your (username) and (password) to generate a newer token with a new expiration date.

3. To add countries as a subscription go to /api/add/, you need to send a list of "countryName" using the Slug format, example: {"countryName": ["yemen" ,"suriname","taiwan" ] }

4. To view the details of the countries, you can either call /api/view/ or using the management command "showcases {username}".

5. To calculate the percentage of recovered over confirmed, go to /api/percentage/ and add the country in the request body like: "South Africa" (not Slug format)

5. To get the top 3 countries in a specific case, insert the case in the body and go to /api/top3/, cases are: "confirmed", "deaths" , "recovered". (Recovered is not implemented due to /summary link giving 0's in every single country, 
so I tried looping through every single country with the last available recovered value and I got this message: 
{'message': 'Too Many Requests on /total/dayone/country/latvia. Please upgrade to a subscription at https://covid19api.com/#subscribe', 'success': False})

6. Top 3 Countries with dates is impossible since the API's cases are additive meaning if I extract the cases from today, it will be the cases of every single previous day + today.




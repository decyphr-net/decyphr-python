"""
The accounts app.

The accounts will handle a couple of different scenarios, which are:

  - store basic user information, such as the users name, email, password, etc
    so that a user can be indentified and authorized within the application
  - store any preferences that a user may have about how they interact with the
    application, such as the language that they would like to read the site in
  - store information about how often the user is logging in. This will 
    us to award a user for logging everyday, and it will also allow us to send
    reminders to users to remind them to come back to the site in the event
    that they haven't accessed the platform in some time

The authentication system is token based. When a user creates an account, a
token will be generated for them. After both registration and login, the token
will be returned to the requesting client to enable authentication to be
performed on all API calls that require authentication.

In addition to this, we will need to be able to store additional information
about the user and their login habits. In order to achieve this, we had to
build a custom view that handles the login process, rather than using the view
that the DRF provides out of the box.

The first version of this app should provide the following functionality:
  - User registration
    - Validate incoming data
    - Create the user profile
    - Generate the user's token
    - Send a confirmation email
    - Return token to client
  - User login
    - Validate incoming data
    - Authenticate user
    - Return token to client
  - User logout
    - Log user out
    - Return message to the client
  - User profiles
    - Users should be able to view their profiles, update any aspect of the
    profile and even delete the profile if they choose
  - Password reset
    - Send an email to the user as confirmation
    - Validate the incoming data
    - Update the password
"""
# LangApp

LangApp is designed to assist users that are learning to read in new languages.

The idea is that a user that is reading a book in a new language will need to translate some text to their native language to understand the text. LangApp will provide the user with the translation and an audio file to listen to how the text should sound.

## Technical Documentation
This part of the project is built as a series of APIs.

Some of the main endpoints are:

### `/token-auth/`
Returns the user's JWT. This is effectively logging the user in and returns the token that will be used to authenticate all subsequent requests

### `/user/register/`
Register a new user when a new user wishes to sign up for the site. This endpoint requires a user's email, username, first and last names, and the user's password

### `/user/current-user/` - Requires authentication
Get the full profile for the currently logged in user

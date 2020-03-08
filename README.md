# Decyphr
Decyphr is designed to assist users that are learning to read in new languages.

A user that is reading a book in a new language will need to translate some text to their native language to understand the text. Decyphr will provide the user with the translation and an audio file to listen to how the text should sound. The user will also receive a breakdown of how the sentence is structured - i.e. a user will be told which words are verbs, adverbs, etc.

The purpose of this is to show a user to learn how sentences are structured within the texts that they translate, and hear how the text is supposed to be pronounced, empowering the user to become more comfortable with the language that they are learning.

- [Decyphr](#decyphr)
  - [Goals](#goals)
    - [Initial Goals](#initial-goals)
  - [Technical Documentation](#technical-documentation)
    - [`/token-auth/`](#token-auth)
    - [`/user/register/`](#userregister)
    - [`/user/current-user/` - Requires authentication](#usercurrent-user---requires-authentication)

## Goals
Below I've detailed a list of the initial goals of Decyphr, as well as some goals that we hope to achieve with this project.

### Initial Goals
  - Translation services. This should include the following:
    - Translate the text from the language that the user is learning into their native language
    - Show a historical record of the items that a user has translated so they may review them at a later point
    - Provide an audio file with an example of the pronunciation of the original text for the user to hear how the text should sound in the language that they are trying to learn
    - Provide an analysis of the text that they've translated to, so the user can which words are verbs, adverbs, etc

## Technical Documentation
This part of the project is built as a series of APIs.

Some of the main endpoints are:

### `/token-auth/`
Returns the user's JWT. This is effectively logging the user in and returns the token that will be used to authenticate all subsequent requests

### `/user/register/`
Register a new user when a new user wishes to sign up for the site. This endpoint requires a user's email, username, first and last names, and the user's password

### `/user/current-user/` - Requires authentication
Get the full profile for the currently logged in user

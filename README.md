# Description
This api is a basic implementation that works with Slack. The api is primarily used to lay the ground work for setting up slack integration with a Django project. Here you will find how to subscribe to events in slack, pass the slack challenge for event subscription using slack's recommended security procedures, and using interactivity with shortcuts in slack using slacks modals.

## Set up instructions
You will need python installed on your machine (you can get that from [here](https://www.python.org/)) and an IDE of your choice I use [PyCharm](https://www.jetbrains.com/pycharm/)
1. Download ngrok from [here](https://ngrok.com/download)
1. Set up your virtual enviornment [here](https://realpython.com/python-virtual-environments-a-primer/) is a great guide on this from the guys at Real Python
1. run the following pip installs in your virual enviornment
  * ``` pip install Django ```
  * ``` pip install djangorestframework ```
  * ``` pip install python-dotenv ```
  * ``` pip install slack-sdk ```
  * ``` pip install aiohttp ```
4. In a terminal cd into the directory where your ngrok was installed and run ``` ./ngrok http 8000 ``` (Note this is for linux) check ngrok for how to do it on windows/mac
5. In the [settings.py](https://github.com/forrestpatwalker/slack_bot/blob/master/slackbot/slackbot/settings.py) file you will need to change the ALLOWED_HOSTS on line 28 to your own ngrok proxy without the https://. Without this you may get an error when you try to run things.
6. Open up your project in your IDE, open your IDE's terminal, and cd into the slackbot folder then run ``` python manage.py migrate ``` then ``` python mange.py runserver ``` this will start up the django localserver at port 8000 (it might be a different port for you so adjust accordingly)
7. find your slack apps credentials for Bot User OAuth Token and Signing Secret and save those values in a .env file located in the root directory of the project. These values should not have quotation marks or spaces, for example mine were SLACK_SIGNING_SECRET=token and SLACK_BOT_USER_ACCESS_TOKEN=token
8. In your slack app settings go to the Interactivity & Shortcuts tab and turn it on, the Request URL is where slack will send the payload of data to. This will be your ngrok forwarding link with /slack/commands/ for example mine was https://2c2f67b6eac9.ngrok.io/slack/commands/ (this link wont go to anything). You will need to change this everytime you start your ngrok proxy because only premium ngrok users will have the same link every time.
9. Create a shortcut for your app this will be how your slack app sends a payload to you.

## How the code works
in the url files you will find the paths I have created for this app there are /slack/offers/ and /slack/commands/ both of the code for these endpoints can be found in the [views.py](https://github.com/forrestpatwalker/slack_bot/blob/master/slackbot/events/views.py) file.

The SlackOffers class is used for Event Subscriptions in slack. It overall is recieving a payload of JSON data from slack via a POST request. A part of the subscribing to the Event Subscriptions is passing a challenge that slack sends you. This code does exactly that while using Slacks recommendations for security.

The SlackCommands class is used for a slack shortcut (this class should work if you followed the instructions above). The class recieves a post request from slack once a user on slack uses the apps shortcut. Slack sends a payload to the endpoint and is recieved here. The class checks the payload for a field called 'view' this field will not be present when the user first initiates the slack shortcut, so the else statement will run instead. The else statement sends back a modal to the user to fill out (this is like a form for the user) it also responds with a 200 ok response as slack requires this within 3 seconds of the user using the shortcut. Once the user has filled out the form and submitted it, the endpoint recieves another payload with the data the user just filled out on the slack modal. This payload will have the field 'view' and the app will respond by thanking the user for creating an offer and again responding with a 200 ok response.

## Notes
Ultimately this api doesnt accomplish much but a lot of this information was hard for me to find that utilized django and slack together. I figured my struggles with this could at least help someone else out down the line. A lot of what is here could easily be modified to fit whatever you are going for, and gives a good base to work from.

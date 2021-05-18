# Set up instructions
You will need python installed on your machine (you can get that from [here](https://www.python.org/)) and an IDE of your choice I use [PyCharm](https://www.jetbrains.com/pycharm/)
1. Download ngrok from [here](https://ngrok.com/download)
1. Set up your virtual enviornment [here](https://realpython.com/python-virtual-environments-a-primer/) is a great guide on this from the guys at Real Python
1. run the following pip installs in your virual enviornment
  * ``` pip install Django ```
  * ``` pip install djangorestframework ```
  * ``` pip install python-dotenv ```
  * ``` pip install slack-sdk ```
4. In a terminal cd into the directory where your ngrok was installed and run ``` ./ngrok http 8000 ``` (Note this is for linux) check ngrok for how to do it on windows/mac
1. Open up your project in your IDE and in the terminal run ``` python manage.py runserver ``` this will start up the django localserver at port 8000 (it might be a different port for you so adjust accordingly)
1. find your slack apps credentials for Bot User OAuth Token and Signing Secret and save those values in a .env file located in the root directory of the project. These values should not have quotation marks or spaces, for example mine were SLACK_SIGNING_SECRET=token and SLACK_BOT_USER_ACCESS_TOKEN=token
1. In your slack app settings go to the Interactivity & Shortcuts tab and turn it on the Request URL is where slack will send the payload of data to. This will be your ngrok forwarding link with /slack/commands/ for example mine was https://2c2f67b6eac9.ngrok.io/slack/commands/ (this link wont go to anything). You will need to change this everytime you start your ngrok proxy because only premium ngrok users will have the same link every time.
1. Create a shortcut for your app this will be how your slack app sends a payload to you.

## How the code works

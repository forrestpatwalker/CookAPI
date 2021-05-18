import os
from hashlib import sha256
from hmac import new, compare_digest
from time import time
import json
from dotenv import load_dotenv
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from slack import WebClient


class SlackOffers(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        load_dotenv()
        request_body = request.body.decode('UTF-8')
        json_body = json.loads(request_body)
        timestamp = int(request.headers['X-Slack-Request-Timestamp'])
        slack_signature = request.headers['X-Slack-Signature']

        # Check Timestamp to protect against replay attacks
        if abs(time() - timestamp) > 60 * 5:
            return HttpResponse(status=403)

        # Concatenate the version number, timestamp, and request body together with a : as a delimiter
        sig_basestring = 'v0:' + str(timestamp) + ':' + request_body

        # Encode the data
        byte_key = bytes(os.environ.get('SLACK_SIGNING_SECRET'), 'UTF-8')
        message = sig_basestring.encode()

        # Hash data and store as a hex digest of the hash
        my_signature = new(byte_key, message, sha256).hexdigest()

        # Compare keys and if true solve Slacks challenge to verify the api endpoint
        if compare_digest(bytes('v0=' + my_signature, 'UTF-8'), bytes(slack_signature, 'UTF-8')):
            if 'type' in json_body:
                if json_body['type'] == 'url_verification':
                    response_dict = {"challenge": json_body['challenge']}
                    return JsonResponse(response_dict, safe=False)

        return HttpResponse(status=403)


class SlackCommands(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = json.loads(request.POST['payload'])
        load_dotenv()
        client = WebClient(token=os.environ.get('SLACK_BOT_USER_ACCESS_TOKEN'))

        # This will only run when the modal is submitted by the slack user.
        if 'view' in data:
            print(json.dumps(data, indent=4, sort_keys=True))
            user_id = data['user']['id']

            # With the user id we request information from slack about the user and store it.
            user_information = client.users_info(user=user_id)
            user_email = user_information['user']['profile']['email']

            # Store submitted values
            input_title = data['view']['state']['values']['title_block']['title_action']['value']
            input_description = data['view']['state']['values']['description_block']['description_action']['value']
            input_public = data['view']['state']['values']['public_choice_block']['public_choice_action']['selected_option']['value']

            # Respond with a message in the testing channel
            client.chat_postMessage(channel='testing', text="Thanks for creating an offer!")
            return HttpResponse(status=200)

        # This will run when a slack user uses the Create offer shortcut.
        else:
            # This is the modal that the user on slack will receive and fill out.
            view = {
                "title": {
                    "type": "plain_text",
                    "text": "Create an Offer"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit"
                },
                "type": "modal",
                "close": {
                    "type": "plain_text",
                    "text": "Cancel"
                },
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "title_block",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "title_action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Title"
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "description_block",
                        "element": {
                            "type": "plain_text_input",
                            "multiline": True,
                            "action_id": "description_action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Description"
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "public_choice_block",
                        "element": {
                            "type": "radio_buttons",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Make this offer public"
                                    },
                                    "value": "public"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Make this offer private"
                                    },
                                    "value": "private"
                                }
                            ],
                            "action_id": "public_choice_action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Public"
                        }
                    }
                ]
            }

            # This sends the modal and trigger_id to slack to open the modal for the slack user.
            client.views_open(trigger_id=data['trigger_id'], view=view)
            return HttpResponse(status=200)

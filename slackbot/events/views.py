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
        if 'view' in data:
            client.chat_postMessage(channel='testing', text="Thanks for creating an offer!")
            return HttpResponse(status=200)

        else:
            view = {
                "title": {
                    "type": "plain_text",
                    "text": "What's Cookin'",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "type": "modal",
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "blocks": [
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "plain_text_input-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Title",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "multiline": True,
                            "action_id": "plain_text_input-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Description",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "checkboxes",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Please display this offer publicly",
                                        "emoji": True
                                    },
                                    "value": "value-0"
                                }
                            ],
                            "action_id": "checkboxes-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Public",
                            "emoji": True
                        }
                    }
                ]
            }

            client.views_open(trigger_id=data['trigger_id'], view=view)
            return HttpResponse(status=200)

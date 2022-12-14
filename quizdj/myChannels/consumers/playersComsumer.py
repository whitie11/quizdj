# chat/consumers.py
import datetime
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from urllib.parse import parse_qs

from django.http import JsonResponse

from ..models import Active_Channel, Active_ChannelSerializer


class QuizConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_active_channel(self, username, userID, channel_name, room_group_name,):
        new_channel = Active_Channel.objects.create(
            username=username,
            userID = userID,
            channel_name=channel_name,
            quiz_group_name=room_group_name,
            lastSeen=datetime.datetime.now()
        )
        new_channel.save()
        return new_channel

    @database_sync_to_async
    def delete_active_channel(self, channel_name):
        Active_Channel.objects.filter(channel_name=channel_name).delete()

    @database_sync_to_async
    def setHandshake(self, channel_name):
        print('About to set Handshake')
        try:
            obj: Active_Channel = Active_Channel.objects.get(
                channel_name=channel_name)
            if obj:
                obj.lastSeen = datetime.datetime.now()
                obj.save()
        except:
            print('Active channel not found in log!')

    async def connect(self):
        params = parse_qs(self.scope["query_string"])
        # print(params)
        token = parse_qs(self.scope["query_string"].decode("utf8"))["token"][0]
        # print(token)
        self.username = parse_qs(self.scope["query_string"].decode("utf8"))[
            "username"][0]
        # print(token)
        self.userID = parse_qs(self.scope["query_string"].decode("utf8"))[
            "userID"][0]
        self.room_name = parse_qs(self.scope["query_string"].decode("utf8"))[
            "room_name"][0]
        # print(self.quiz_name )
        self.room_group_name = 'quiz_%s' % self.room_name
        # print(self.channel_name)

        # TODO check if user already connected


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.save_active_channel(self.username, self.userID, self.channel_name,  self.room_group_name)

        await self.accept()
        await self.channel_layer.group_send(
            'quiz_lobby1',
            {'type': 'playersList',
                'subject': 'getPlayers',
             }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.delete_active_channel(self.channel_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            'quiz_lobby1',
            {
                'type': 'playersList',
                'subject': 'getPlayers',
            }
        )

    # Receive message from WebSocket /player
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('message recieved player consumer')
        # message = text_data_json['content']
        print(text_data_json['type'])
        print(self.username)
        if text_data_json['type'] == 'handshake':
            await self.setHandshake(self.channel_name)

        elif text_data_json['subject'] == 'message' and text_data_json['type'] == 'chat_message':
            print('chat message to all players')
            await self.channel_layer.group_send(
                'quiz_lobby',
                {
                    'type': 'chat_message',
                    'content': text_data_json['content'],
                    'source': text_data_json['source'],
                    'subject': 'message',
                    'reciever': text_data_json['reciever']
                }
            )
        # elif text_data_json['subject'] == 'message' and text_data_json['type'] == 'leaderboard':
        #     print('leaderboard msg recieved ')
        #     await self.channel_layer.group_send(
        #         'quiz_lobby',
        #         {
        #             'type': 'leaderboard',
        #             'subject': 'leaderboard',
        #             'leaderboard': text_data_json['leaderboard']
        #         }
        #     )
        elif text_data_json['subject'] == 'answer' and text_data_json['type'] == 'answer':
            # send to QM
            print('sending to QM')
            await self.channel_layer.group_send(
                'quiz_lobby1',
                {
                    'type': text_data_json['type'],
                    'subject': text_data_json['subject'],
                    'source': text_data_json['source'],
                    'userID': text_data_json['userID'],
                    'answer': text_data_json['answer'],
                    'question_ID': text_data_json['question_ID'],
                    'question_num': text_data_json['question_num'],
                    'timeSpent': text_data_json['timeSpent']
                }
            )
            print('echoing back')
            # echo back
            # timeStr = datetime.datetime.fromtimestamp(text_data_json['timeSpent'])
            msg = "You answered question {} with answer {} after {} seconds!".format(
                text_data_json['question_num'],
                text_data_json['answer'],
                text_data_json['timeSpent'],
            )
            await self.send(text_data=json.dumps({
                'type': 'ind_message',
                'subject': 'message',
                'content': msg,
                'source': 'server',
            }))

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                'type': event['type'],
                'subject': event['subject'],
                'source': event['source'],
                'content': event['content'],
                'reciever': event['reciever']
            }
        ))

    async def ind_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'subject': event['subject'],
            'source': event['source'],
            'content': event['content'],
            'reciever': event['reciever']
        }))

    async def question(self, event):
        # send question to all players
        await self.send(text_data=json.dumps(
            {
                'type': 'question',
                'subject': event['subject'],
                'ID': event['ID'],
                'group': event['group'],
                'question_num': event['question_num'],
                'text': event['text'],
                'answerA': event['answerA'],
                'answerB': event['answerB'],
                'answerC': event['answerC'],
                'answerD': event['answerD'],
                'duration': event['duration'],
                'startTime': event['startTime']
            }
        ))

    async def leaderboard(self, event):
        # send leaderboard to all players
        await self.send(text_data=json.dumps(
            {
                'type': 'message',
                'subject': event['subject'],
                'leaderboard': event['leaderboard']
            }
        ))



    async def timer(self, event):
        await self.send(text_data=json.dumps(
            {
                'subject': event['subject'],
                'value': event['value']
            }
        ))

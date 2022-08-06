import datetime
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from ..models import Active_Channel, Active_ChannelSerializer


class QMConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def purgeACdata(self):
        queryTime = datetime.datetime.now()-datetime.timedelta(seconds=60)
        expiredPlayers = Active_Channel.objects.filter(lastSeen__lte=queryTime)
        expiredPlayers.delete()

    @database_sync_to_async
    def getPlayers(self):
        players = Active_Channel.objects.all()
        serialiser = Active_ChannelSerializer(players, many=True)
        return json.dumps(serialiser.data)

    async def connect(self):
        params = parse_qs(self.scope["query_string"])
        print("inQM ")
        token = parse_qs(self.scope["query_string"].decode("utf8"))["token"][0]
        print(token)
        self.room_name = parse_qs(self.scope["query_string"].decode("utf8"))[
            "room_name"][0]
        self.room_group_name = 'quiz_%s' % self.room_name
        print(self.room_name)
        print(self.channel_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from QuizMaster
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print('recieved from QM')
        # send question to players!
        if data['subject'] == 'question':
            await self.channel_layer.group_send(
                'quiz_lobby',
                {
                    'type': 'question',
                    'subject': data['subject'],
                    'ID': data['ID'],
                    'text': data['text'],
                    'answerA': data['answerA'],
                    'answerB': data['answerB'],
                    'answerC': data['answerC'],
                    'answerD': data['answerD'],
                    'time': data['time'],
                }
            )
        elif data['subject'] == 'timer':
            await self.channel_layer.group_send(
                'quiz_lobby',
                {
                    'type': 'timer',
                    'subject': data['subject'],
                    'value': data['value']
                }
            )
        elif data['subject'] == 'getPlayers':
            await self.purgeACdata()
            self.p = await self.getPlayers()
            await self.send(text_data=json.dumps(
                {
                    'type': 'playersList',
                    'playersList': self.p
                }
            ))

    async def answer(self, event):
        # Send answer recieved from player to QM
        print('answer recieved!!!!!')
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'subject': event['subject'],
            'source': event['source'],
            'answer': event['answer'],
            'question_no': event['question_no'],
            'timeSpent': event['timeSpent']
        })
        )

    async def playersList(self, event):
        # Send players to QM
        print(event)
        await self.purgeACdata()
        self.p = await self.getPlayers()
        await self.send(text_data=json.dumps({
            'type': 'playersList',
            'subject': 'playersList',
            'playersList': self.p
        })
        )

import slixmpp
import asyncio

class XMPPMessageRouter(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            message_body = msg['body'].strip().

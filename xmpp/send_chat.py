import slixmpp
import asyncio

class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        super().__init__(jid, password)

        # The message to send and recipient
        self.recipient = recipient
        self.msg = message

        # Event handlers
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()  # Send online presence
        await self.get_roster()  # Request roster to ensure we're connected

        # Send the message and disconnect
        self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
        self.disconnect()

def send_xmpp_message(jid, password, recipient, message):
    xmpp = SendMsgBot(jid, password, recipient, message)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process(forever=False)

# Example usage
jid = 'yourusername@xmppserver.com'  # Your full JID (username@server)
password = 'yourpassword'
recipient = 'recipient@xmppserver.com'  # Recipient's JID
message = 'Hello, this is a test message.'

# As this is an async function, it should be run in an event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(send_xmpp_message(jid, password, recipient, message))

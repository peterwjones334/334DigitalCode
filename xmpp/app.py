from flask import Flask, request, jsonify
import asyncio
from slixmpp import ClientXMPP

app = Flask(__name__)

class SendMsgBot(ClientXMPP):
    def __init__(self, jid, password, recipient, msg):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = msg
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
        self.disconnect()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    jid = data['jid']
    password = data['password']
    recipient = data['recipient']
    message = data['message']

    xmpp = SendMsgBot(jid, password, recipient, message)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0199')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(xmpp.connect())
    xmpp.process(forever=False)

    return jsonify({"message": "Message sent successfully"})

if __name__ == '__main__':
    app.run(debug=True)

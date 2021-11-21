import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import datetime
import uuid

class testAgent(Agent):
    class RecvBehav(PeriodicBehaviour):
        async def run(self):
            # print("RecvBehav running")

            msg = await self.receive(timeout=1)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
                f = open('logs.txt', 'a')
                f.write(f'{msg.to} RECEIVED message with content "{msg.body}" from {msg.sender} at {datetime.datetime.now()}\n')
                f.close()

    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="MA_agent1@01337.io")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"  # Set the message content
            await self.send(msg)
            print("Message sent!")

            f = open('logs.txt', 'a')
            f.write(f'{msg.sender} SENDS message with content "{msg.body}" to {msg.to} at {datetime.datetime.now()}\n')
            f.close()

    async def setup(self):
        print("Agent started")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        InformBehav = self.InformBehav(period=100, start_at=start_at)
        RecvBehav = self.RecvBehav(period=100, start_at=start_at)
        self.add_behaviour(InformBehav)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(RecvBehav, template)
        print(self.presence.get_contacts())


def createAgent(agent_name, agent_pass):
    agent = testAgent(agent_name, agent_pass)
    future = agent.start()
    future.result()

    return agent

def getFullName(agent):
    return agent.name+"@01337.io"
if __name__ == "__main__":
    agent1 = createAgent("MA_agent1@01337.io", "Pass_agent1")
    # agent2 = createAgent("MA_agent2@01337.io", "Pass_agent2")
    # agent3 = createAgent("MA_agent3@01337.io", "Pass_agent3")
    # agent4 = createAgent("MA_agent4@01337.io", "Pass_agent4")
    # agent5 = createAgent("MA_agent5@01337.io", "Pass_agent5")
    # agent6 = createAgent("MA_agent6@01337.io", "Pass_agent6")

    print(getFullName(agent1))
    # agent1.presence.subscribe("MA_agent2@01337.io")
    # agent1.presence.subscribe("MA_agent2@01337.io")

    while agent1.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # senderagent.stop()
            agent1.stop()
            break
    print("Agents finished")
    # dummy = DummyAgent("MA_agent1@01337.io", "Pass_agent1")
    # dummy = DummyAgent("MA_agent2@01337.io", "Pass_agent2")

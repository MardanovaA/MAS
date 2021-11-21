import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import datetime

class testAgent(Agent):
    class RecvBehav(PeriodicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                # Запись в логи
                print(f'{msg.to} RECEIVED message with content "{msg.body}" from {msg.sender} at {datetime.datetime.now()}')
                f = open('logs.txt', 'a')
                f.write(f'{msg.to} RECEIVED message with content "{msg.body}" from {msg.sender} at {datetime.datetime.now()}\n')
                f.close()

    class InformBehav(PeriodicBehaviour):
        async def run(self):
            if self.get('msg'):
                # Отправка
                ms = self.get('msg')
                msg = Message(to=ms['to'])  # Instantiate the message
                msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                msg.body = ms['message']  # Set the message content
                await self.send(msg)
                print(f'{msg.sender} SENDS message with content "{msg.body}" to {msg.to} at {datetime.datetime.now()}')

                # Запись в логи
                f = open('logs.txt', 'a')
                f.write(f'{msg.sender} SENDS message with content "{msg.body}" to {msg.to} at {datetime.datetime.now()}\n')
                f.close()

                # Очищение
                self.set('msg', None)

    async def setup(self):
        self.presence.approve_all = 'True'
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        InformBehav = self.InformBehav(period=10, start_at=start_at)
        RecvBehav = self.RecvBehav(period=10, start_at=start_at)
        self.add_behaviour(InformBehav)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(RecvBehav, template)


def createAgent(agent_name, agent_pass):
    agent = testAgent(agent_name, agent_pass)
    future = agent.start()
    future.result()

    return agent

def getFullName(agent):
    return agent.name+"@01337.io"


if __name__ == "__main__":
    # Создание агентов
    A1 = createAgent("MA_agent1@01337.io", "Pass_agent1")
    A2 = createAgent("MA_agent2@01337.io", "Pass_agent2")
    A3 = createAgent("MA_agent3@01337.io", "Pass_agent3")
    A4 = createAgent("MA_agent4@01337.io", "Pass_agent4")
    A5 = createAgent("MA_agent5@01337.io", "Pass_agent5")
    A6 = createAgent("MA_agent6@01337.io", "Pass_agent6")

    # Отправка сообщенияя
    fr = {'message': 'message', 'to': getFullName(A3)}
    A1.set('msg', fr)

    # Удаление
    while A1.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            A1.stop()
            A2.stop()
            A3.stop()
            A4.stop()
            A5.stop()
            A6.stop()
            break
    print("Agents finished")

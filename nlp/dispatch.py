"""
Module interprets agent commands and dispatches an action
"""
import json
import typing


def on_message(client, obj, msg):
    print('on msg: ' + str(msg))
    try:
        json_string = str(msg.payload, 'utf-8')
        payload = json.loads(json_string)
    except json.decoder.JSONDecodeError:
        return

    cmd = interp_command(payload.get('command', 'default'), list(dispatcher.keys()))

    dispatcher[cmd](payload)


def interp_command(cmd_str: str, actions: typing.List[str]) -> str:
    """Output a discrete action to take from a user command in natural language.
    
    Args:
        cmd_str: user command
        actions: list of commands available from dispatcher 

    Returns:
        str: single command for dispatcher to execute

    Examples:
        >>> interp_command('describe what is around me', ['describe','count'])
        'describe'
        >>> interp_command('count the number of objects in view', ['describe', 'count'])
        'count'
    """

    # faster, but less readable
    # return next((axn for axn in actions if axn in cmd_str), 'default')

    for axn in actions:
        if axn in cmd_str:
            return axn
    return 'default'


class Dispatchable():
    from nlp.mqtt import mqttc, AI_TOPIC

    client = mqttc
    topic = AI_TOPIC

    def send(self, payload):
        self.client.publish(self.topic, payload)


class Echo(Dispatchable):
    def __call__(self, msg):
        self.send(json.dumps(msg))


class NoOp(Dispatchable):
    def __call__(self, msg):
        pass


dispatcher = {
    'default': NoOp(),
    'debug': Echo(),
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()

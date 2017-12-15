from nlp import describe_state
from nlp.dispatch import Dispatchable


class DescribeColor(Dispatchable):

    color_tmpl = "The {} is primarily {}"

    def __init__(self, state_q):
        self.state_q = state_q

    def __call__(self, payload):
        state = self.state_q.get()

        if state:

            obj_name, object_data = state.popitem()

            if object_data:
                color_freq = object_data[0]['color']

                max_color = color_freq.idxmax()

                print(state)
                self.send({'response': self.color_tmpl.format(obj_name, max_color)}, subtopic=['say'])



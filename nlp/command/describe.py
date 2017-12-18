from nlp import describe_state
from nlp.dispatch import Dispatchable


class Describe(Dispatchable):

    obj_desc_tmpl = '{num_obj} {obj_color} {obj_name} to your {rel_pos}'

    def __init__(self, state_q):
        self.state_q = state_q

    def __call__(self, payload):
        state = self.state_q.get()

        if state:
            description = describe_state(state)

            self.send({'response': description}, subtopic=['say'])


def count_obj_by_color(state):
    new_state = {k: len(v) for k, v in state.items()}
    return new_state

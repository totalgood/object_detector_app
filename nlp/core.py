""" Natural Language Processing (Generation) utilities """
import collections
import os

import pandas as pd
import object_detection.color_labeler as color_labeler

from nlp.plurals import PLURALS
from collections import defaultdict


def pluralize(s):
    """ Convert word to its plural form.

    >>> pluralize('cat')
    'cats'
    >>> pluralize('doggy')
    'doggies'

    Better:

    >> from pattern.en import pluralize, singularize

    Or, even better, just create pluralized versions of all the class names by hand!
    """
    word = str.lower(s)

    # `.get()` rather than `word in PLURALS` so that we only look up the word once
    pluralized_word = PLURALS.get(word, None)
    if pluralized_word is not None:
        return pluralized_word

    # case = str.lower(s[-1]) == s[-1]
    if word.endswith('y'):
        if word.endswith('ey'):
            return word + 's'
        else:
            return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an') and len(word) > 3:
        return word[:-2] + 'en'
    else:
        return word + 's'


def update_state(boxes, classes, scores, category_index, src_img=None, window=10, max_boxes_to_draw=None, min_score_thresh=.5):
    """ Revise state based on latest frame of information (object boxes)

    TODO(Hobson | Alex) Finish docstring (Need to know all the args and the return val)
    Args:
        boxes (list): 2D numpy array of shape (N, 4): (ymin, xmin, ymax, xmax), in normalized format between [0, 1].
        classes,
    Args (that should be class attributes):
        category_index (dict of dicts): {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'bicycle'},...}
    Returns:

        Example Output:
        {
            "cup":
                 [
                    { color: [<color_vec>] },
                    { color: [<color_vec>] ),
                ],
            "person":
                [
                    { color: [<color_vec>] },
                    { color: [<color_vec>] },
                    { color: [<color_vec>] }
                ],
            ...

        }
    """
    num_boxes = min([boxes.shape[0] if max_boxes_to_draw is None else max_boxes_to_draw, boxes.shape[0], len(classes)])

    if update_state.states is None:
        # Initialize a matrix of state vectors for the past 20 frames
        update_state.i = 0
        update_state.window = 20
        update_state.columns = pd.DataFrame(list(category_index.values())).set_index('id', drop=True)['name']
        update_state.states = pd.DataFrame(pd.np.zeros((20, len(category_index)), dtype=int), columns=update_state.columns)
        update_state.state0 = pd.Series(index=update_state.columns)

    state = []  # if state is None else state
    for i in range(num_boxes):
        if scores is None or scores[i] > min_score_thresh:
            # box = tuple(boxes[i].tolist())
            class_name = category_index.get(classes[i], {'name': 'unknown object'})['name']
            display_str = '{}: {} {}%'.format(classes[i], class_name, int(100 * scores[i]))
            print(display_str)  # TODO(Alex) Convert to logging
            state += [class_name]
    state = collections.Counter(state)
    update_state.states.iloc[i % len(update_state.states), :] = pd.Series(state)
    state = sorted(list(state.items()))
    i = (i + 1) % len(update_state.states)  # update_state.window  TODO(Hobs) Is `i` used after this?
    return state


update_state.states = None

def update_state_dict(image, boxes, classes, scores, category_index, src_img=None, window=10, max_boxes_to_draw=None, min_score_thresh=.5):
    """ Revise state based on latest frame of information (object boxes)

    TODO(Hobson | Alex) Finish docstring (Need to know all the args and the return val)
    Args:
        boxes (list): 2D numpy array of shape (N, 4): (ymin, xmin, ymax, xmax), in normalized format between [0, 1].
        classes,
    Args (that should be class attributes):
        category_index (dict of dicts): {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'bicycle'},...}
    Returns:

        Example Output:
        {
            "cup":
                 [
                    { color: [<color_vec>], score: 0.95, ... },
                    { color: [<color_vec>], score: 0.88, ... ),
                ],
            "person":
                [
                    { color: [<color_vec>], score: 0.99, ... },
                    { color: [<color_vec>], score: 0.75, ... },
                    { color: [<color_vec>], score: 0.85, ... }
                ],
            ...

        }
    """
    num_boxes = min([boxes.shape[0] if max_boxes_to_draw is None else max_boxes_to_draw, boxes.shape[0], len(classes)])

    state_obj = defaultdict(list)
    if update_state_dict.i is None:
       update_state_dict.i = 0

    for i in range(num_boxes):
        if scores is None or scores[i] > min_score_thresh:
            class_name = category_index.get(classes[i], {'name': 'unknown object'})['name']
            display_str = '{}: {} {}%'.format(classes[i], class_name, int(100 * scores[i]))
            print(display_str)  # TODO(Alex) Convert to logging

            obj_data = {
                'score': scores[i],
                'color': color_labeler.estimate(image, box=boxes[i])
            }

            state_obj[class_name] += [obj_data]

    update_state_dict.i += 1

    return state_obj


update_state_dict.i = None

# for i in range(update_state.window):
#     update_state.states.append([])


def describe_state(state):
    """ Convert a state vector dictionary of objects and their counts into a natural language string

    >>> describe_state({'skis': [{'score': 0.99}, {'score': 0.88}]})
    '2 pairs of skis'
    >>> statement = describe_state({'skis': [{'score': 0.88}], 'cup': [{'score': 0.87 }, {'score': 0.66}]} )
    >>> '2 cups' in statement and 'and' in statement and '1 skis' in statement
    True
    """
    def count_objects(state_dict):
        new_dict = {k: len(v) for k, v in state_dict.items()}
        return new_dict

    state_counts = count_objects(state)

    plural_description_list = ['{} {}'.format(i, pluralize(s) if i > 1 else s) for (s, i) in state_counts.items()]

    comma_list = ', '.join(plural_description_list[:-2])
    conjunction = ' and '.join(plural_description_list[-2:])
    if len(comma_list) > 0:
        delim_description = comma_list + ',' + conjunction
    else:
        delim_description = conjunction

    return delim_description


def say(s, rate=230):
    """ Convert text to speech (TTS) and play resulting audio to speakers

    If "say" command is not available in os.system then print the text to stdout and return False.

    >>> say('hello')
    'hello'
    """
    try:
        os.system('say --rate={rate} "{s}"'.format(**dict(rate=rate, s=s)))
        return s
    except:
        print(s)
    return False

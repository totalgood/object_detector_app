# Object-Detector-App

A real-time object recognition application using [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) and [OpenCV](http://opencv.org/).

## Getting Started
1. `conda env create -f environment.yml`
2. `python object_detection_app.py`
    Optional arguments (default value):
    * Show all commands `--help`
    * Device index of the camera `--source=0`
    * Width of the frames in the video stream `--width=480`
    * Height of the frames in the video stream `--height=360`
    * Number of workers `--num-workers=2`
    * Size of the queue `--queue-size=5`
    * URL for video stream `--url=<rstp://...>`
    * Turn on GUI (defaulted to run headless) `--gui`
    * Turn on vocal commands on MacOS (defaulted to silent) `--say`
    * State Buffer Size, how many "states" to capture `--state-queue-size=5`

## Development
### Updating the environment
`conda env update -f environment.yml`

### Tests
```
pytest -vs utils/
python -m pytest
python -m unittest discover -s object_detection -p "*_test.py"
```

### Requirements
- [Anaconda / Python 3.5](https://www.continuum.io/downloads)
- [TensorFlow 1.2](https://www.tensorflow.org/)
- [OpenCV 3.0](http://opencv.org/)

### API 
Our API is accessible via the MQTT protocol.

#### `nsf/explorer/command`
We subscribe to a topic coming from an Android client. Incoming messages should be encoded as JSON objects that match
the following format: 

```json
{
  "id": 123,
  "datetime": 1234123412341234,
  "command": "describe what is going on around me" 
  //...
}
```

#### `nsf/ai/#`
We publish to the root topic and to one or more subtopics. Subtopics will be related to the 
commands that ought be executed on the client. For instance, if we expect the client to read the 
text response aloud, we will publish it in the `say` subtopic (i.e. `nsf/ai/say`). 

Messages should be encoded as JSON objects in the following format: 

```json
{
  "id": 124, // ID for the current payload
  "command_id": 123, // ID of command payload (payload this is in response to)
  "datetime": 1234123412341234,
 
  // Was the service successful?
  "status": {
    "code": 200,
    "message": "success" 
  },
  
  // Prefer kwargs to args
  "args": ["arg1", "arg2", "arg3"], 
  "kwargs": {
    "key1": 1,
    "key2": "kwarg2"
  }
  
  //...
}
```

Here is an example of a response for "say":
Topic: `nsf/ai/say`
Payload: 
```json
{
  "id": 124, 
  "command_id": 123,
  "datetime": 1234123412341234,
  "status": {
    "code": 200,
    "message": "success"
  },
  "args": [], 
  "kwargs": {
    "text": "there is 1 person and a chair around you"
  }
}
```


## Notes
- ~~OpenCV 3.1 might crash on OSX after a while, so that's why I had to switch to version 3.0. See open issue and solution [here](https://github.com/opencv/opencv/issues/5874).~~
- Moving the `.read()` part of the video stream in a multiple child processes did not work. However, it was possible to move it to a separate thread.

## Copyright
See [LICENSE](LICENSE) for details.

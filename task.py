from dataclasses import dataclass


def getTask(name: str):
    _task_registry = {
        "Place Cube": PlaceCubeTask(),
        "Insertion": InsertionTask(),
        "Build Pyramid": PyramidTask(),
    }
    return _task_registry[name]


@dataclass
class Task:
    title: str
    description: str
    image_path: str
    video_path: str
    stages: dict[str, str]


class PlaceCubeTask(Task):
    def __init__(self):
        super().__init__(
            title="Place Cube",
            description='Grab the red stick and position it exactly on the target represented by a blue circle.',
            image_path='/static/proxy-image.png',
            video_path='',
            stages={
                "stage 1": "Orientation Red Stick: Fixed; Goal Position: Fixed",
                "stage 2": "Orientation Red Stick: Random; Goal Position: Fixed",
                "stage 3": "Orientation Red Stick: Random; Goal Position: Random",
            }
        )


class InsertionTask(Task):
    def __init__(self):
        super().__init__(
            title="Insertion",
            description='Hebe den roten Stabe und das Blaue Rohr an und schiebe den roten Stab in das blaue Rohr.',
            image_path='/static/proxy-image.png',
            video_path='',
            stages={
                "stage 1": "Gleiche Orientierung, feste Zuteilung: links: blaues Rohr, rechts: roter Stab",
                "stage 2": "Zufällige Orientierung, feste Zuteilung: links: blaues Rohr, rechts: roter Stab",
                "stage 3": "Zufällige Orientierung, Objeckte zufällig platziert",
            }
        )

class PyramidTask(Task):
    def __init__(self):
        super().__init__(
            title="Build Pyramid",
            description='Stack the dice. The red cube should be at the bottom, the yellow cube in the middle, and the green cube on top.',
            image_path='/static/proxy-image.png',
            video_path='',
            stages={
                "stage 1": "TODO",
                "stage 2": "TODO",
                "stage 3": "TODO",
            }
        )

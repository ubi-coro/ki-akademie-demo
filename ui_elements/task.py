from dataclasses import dataclass

class TaskName:
    PLACE_CUBE = 'Pick and Place'
    INSERTION = 'Insertion'
    BUILD_PYRAMID = 'Tower Stacking'

tasks = [TaskName.PLACE_CUBE, TaskName.INSERTION, TaskName.BUILD_PYRAMID]

def getTask(name: str):
    _task_registry = {
        TaskName.PLACE_CUBE: PlaceCubeTask(),
        TaskName.INSERTION: InsertionTask(),
        TaskName.BUILD_PYRAMID: PyramidTask(),
    }
    return _task_registry[name]


@dataclass
class Task:
    title: str
    description: str
    user_task: str
    image_path: str
    video_path: str
    stages: dict[str, str]


class PlaceCubeTask(Task):
    def __init__(self):
        super().__init__(
            title=TaskName.PLACE_CUBE,
            description='Grab the red stick and position it exactly on the target represented by a blue circle.',
            user_task='Play around with the task difficulty and the data the AI-model is trained on.',
            image_path='/static/pick_and_place.png',
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
            title=TaskName.INSERTION,
            description='Pick up the red rod and the blue tube, then insert the red rod into the blue tube.',
            user_task='Try solving the task yourself, then watch the AI model perform it. What challenges do you encounter? When and why does the model fail?',
            image_path='/static/insertion.png',
            video_path='',
            stages={
                "stage 1": "Fixed orientation, fixed position assignment: left – blue tube, right – red rod",
                "stage 2": "Random orientation, fixed position assignment: left – blue tube, right – red rod",
                "stage 3": "Random orientation, random assignment",
            }
        )

class PyramidTask(Task):
    def __init__(self):
        super().__init__(
            title=TaskName.BUILD_PYRAMID,
            description='Stack the cubes. The red cube should be at the bottom, the yellow cube in the middle, and the green cube on top.',
            user_task='Try solving the task yourself, then watch the AI model perform it. What challenges do you encounter? When and why does the model fail?',
            image_path='/static/stacking.png',
            video_path='',
            stages={
                "stage 1": "TODO",
                "stage 2": "TODO",
                "stage 3": "TODO",
            }
        )

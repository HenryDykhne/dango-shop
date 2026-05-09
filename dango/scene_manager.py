class SceneManager:
    def __init__(self):
        self.current = None

    def switch(self, new_scene):
        self.current = new_scene

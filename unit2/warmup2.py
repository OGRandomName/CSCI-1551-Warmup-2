from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import random, math
from panda3d.core import ClockObject

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        # Orbit camera parameters
        self.camera_distance = 25
        self.camera_height = 15
        self.taskMgr.add(self.orbit_camera_task, "orbit_camera")

        # Scroll wheel zoom
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)

        # Quit game with ESC
        self.accept("escape", self.quit_game)

        # Load player model
        self.player = self.loader.loadModel("Assets/sphere.egg")
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.setPos(0, 0, 0)

        # Movement keys
        self.key_map = {"w": False, "a": False, "s": False, "d": False}

        self.accept("w", self.set_key, ["w", True])
        self.accept("w-up", self.set_key, ["w", False])
        self.accept("a", self.set_key, ["a", True])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("s", self.set_key, ["s", True])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("d", self.set_key, ["d", True])
        self.accept("d-up", self.set_key, ["d", False])

        # Add movement task
        self.taskMgr.add(self.player_movement_task, "player_movement")

        # Parent object for all cubes
        self.cube_parent = self.render.attachNewNode("CubeParent")

        # Create home base ring
        self.create_home_base_ring(
            model_path="Assets/cube.egg",
            count=20,
            radius=8,
            gap_index=random.randint(0, 19)
        )

    def set_key(self, key, value):
        self.key_map[key] = value

    def player_movement_task(self, task):
        dt = ClockObject.getGlobalClock().getDt()
        speed = 10 * dt

        # Camera-relative movement
        cam_forward = self.camera.getQuat(self.render).getForward()
        cam_right = self.camera.getQuat(self.render).getRight()

        cam_forward.setZ(0)
        cam_right.setZ(0)
        cam_forward.normalize()
        cam_right.normalize()

        move_vec = cam_forward * 0

        if self.key_map["w"]:
            move_vec += cam_forward * speed
        if self.key_map["s"]:
            move_vec -= cam_forward * speed
        if self.key_map["a"]:
            move_vec -= cam_right * speed
        if self.key_map["d"]:
            move_vec += cam_right * speed

        self.player.setPos(self.player.getPos() + move_vec)
        return Task.cont

    def orbit_camera_task(self, task):
        angle = task.time * 0.5
        x = math.cos(angle) * self.camera_distance
        y = math.sin(angle) * self.camera_distance
        self.camera.setPos(x, y, self.camera_height)
        self.camera.lookAt(self.player)
        return Task.cont

    def zoom_in(self):
        self.camera_distance = max(5, self.camera_distance - 1)

    def zoom_out(self):
        self.camera_distance = min(60, self.camera_distance + 1)

    def create_home_base_ring(self, model_path, count, radius, gap_index):
        for i in range(count):
            if i == gap_index:
                continue

            angle = (2 * math.pi / count) * i
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            placeholder = self.cube_parent.attachNewNode("Placeholder2")
            placeholder.setPos(x, y, 0)

            cube = self.loader.loadModel(model_path)
            cube.reparentTo(placeholder)
            cube.setScale(0.5)
            cube.setColor(random.random(), random.random(), random.random(), 1)

    def quit_game(self):
        print("Exiting game...")
        self.userExit()

game = Game()
game.run()
    
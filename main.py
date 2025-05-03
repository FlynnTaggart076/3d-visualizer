from lab_objects import *
from camera import *
from projection import *
import pygame as pg

class SoftwareRenderer:
    def __init__(self):
        pg.init()

        # S_W, S_H = 

        self.RES = self.WIDTH, self.HEIGHT = 1400, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.font = pg.font.SysFont("Arial", 18)
        self.press_check = {"U" : False, "D" : False, "L" : False, "R" : False}

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        
        self.color_vectror = Vector([-1, 2, -3])
        self.objects = []
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0.1, 2, -10])
        self.projection = Projection(self)

        #########################################################################
        # oct1 = Octaeder(self, 2)
        # oct1.translate([2, 0, -3])
        
        # sp1 = Sphere(self, 2, 2)
        # sp1.translate([0, 0, 3])
        # sp2 = Sphere(self, 2, 3)
        # sp2.translate([3, 0, 3])
        
        # origin = Origin(self)

        # self.objects.append(origin)
        # self.objects.append(oct1)
        # self.objects.append(sp1)
        # self.objects.append(sp2)
        #########################################################################


        ###############################   UNUSED   ##############################
        # a = Variant_1(self, subdivisions=50, one_side_polygons=False)
        # self.objects.append(a)

        # b = Variant_4(self, subdivisions=500)
        # self.objects.append(b)
        #########################################################################

        ############################### Variant_1 ###############################
        xf = lambda a, b, u, v : (a + b * math.cos(v)) * math.cos(u)
        yf = lambda a, b, u, v : (a + b * math.cos(v)) * math.sin(u)
        zf = lambda a, b, u, v : b * math.sin(v) + a * u
        params = LabObjectParams(3.0, 1.0, 0.2, 0.1, (0.0, 4 * math.pi), (0.0, 2 * math.pi), (50, 50), xf, yf, zf)
        labObj = LabObject(self, params)
        ########################################################################

        ############################### Variant_4 ###############################
        # xf = lambda a, b, u, v : a * u * math.cos(u)
        # yf = lambda a, b, u, v : b * u * math.sin(u)
        # zf = lambda a, b, u, v : v
        # params = LabObjectParams(1.0, 1.0, 0.1, 0.1, (math.pi / 4, 4 * math.pi), (-2.0, 2.0), (500, 1), xf, yf, zf)
        # labObj = LabObject(self, params)
        #########################################################################

        # self.objects.append(labObj)

    def draw_camera_info(self):
        pos = self.camera.position.matrix[0][:3]
        info_text = f"Pos: {pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f} | Yaw: {self.camera.yaw:.2f}, Pitch: {self.camera.pitch:.2f}"
        text_surface = self.font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, self.HEIGHT - text_surface.get_height() - 10))

        if len(self.objects) == 1:
            a, b = self.objects[-1].params.a, self.objects[-1].params.b
            obj_info_text = f"A: {a}  B: {b}"
            text_surface2 = self.font.render(obj_info_text, True, (255, 255, 255))
            self.screen.blit(text_surface2, (10, self.HEIGHT - text_surface2.get_height() - 30))

    def draw(self):

        # self.objects[-1].rotate_z(math.sin(self.clock.get_time() * 0.001))

        self.screen.fill('skyblue')
        all_faces = []
        for obj in self.objects:
            faces = obj.get_faces()
            all_faces.extend(faces)
        all_faces.sort(key=lambda face: face[0], reverse=True)
        for depth, polygon, color in all_faces:
            pg.draw.polygon(self.screen, color, polygon)
            # self.draw_polygon(self.screen, polygon, color)
    
    def draw_polygon(self, surface, polygon, color = (0, 0, 0)):
        for i in range(len(polygon)):
            start = polygon[i]
            end = polygon[(i + 1) % len(polygon)]
            pg.draw.line(surface, color, start, end, 1)

    def object_control(self):
        keys = pg.key.get_pressed()

        da, db = 0, 0

        if keys[pg.K_UP]:
            if self.press_check["U"]:
                pass
            else:
                self.press_check["U"] = True
                db = 1
        else:
            self.press_check["U"] = False
        
        if keys[pg.K_DOWN]:
            if self.press_check["D"]:
                pass
            else:
                self.press_check["D"] = True
                db = -1
        else:
            self.press_check["D"] = False

        if keys[pg.K_LEFT]:
            if self.press_check["L"]:
                pass
            else:
                self.press_check["L"] = True
                da = -1
        else:
            self.press_check["L"] = False

        if keys[pg.K_RIGHT]:
            if self.press_check["R"]:
                pass
            else:
                self.press_check["R"] = True
                da = 1
        else:
            self.press_check["R"] = False

        if(da != 0) or (db != 0):
            self.objects[-1].change_ab_params(da, db)

    def run(self):
        while True:
            self.draw()
            self.draw_camera_info()
            self.camera.control()
            
            if len(self.objects) == 1:
                self.object_control()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return

            # pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":

    renderer = SoftwareRenderer()  
    renderer.run()
import pygame as pg
from matrix_functions import *

class Object3D:
    def __init__(self, renderer, vertices, faces, one_side_polygons = True, color_sensetivity = True, default_color = (255, 0, 0)):
        self.renderer = renderer
        self.vertices = vertices
        self.faces = faces
        self.one_side_polygons = one_side_polygons
        self.color_sensetivity = color_sensetivity
        self.default_color = default_color

        self.a = None
        self.b = None
        self.a_step = None
        self.b_step = None

    
    def draw(self):
        self.screen_projection()


    def any_func_nested(self, arr, a, b):
        for vertex in arr:
            for coord in vertex:
                if coord == a or coord == b:
                    return True
        return False

    def get_faces(self):
        faces_list = []
        cam_vertices = [vertex * self.renderer.camera.camera_matrix() for vertex in self.vertices]
        proj_vertices = []
        for v in cam_vertices:
            v_proj = v * self.renderer.projection.projection_matrix
            w = v_proj.matrix[0][-1]
            if w != 0:
                coords = [x / w for x in v_proj.matrix[0]]
            else:
                coords = v_proj.matrix[0]
            coords = [0 if (x > 2 or x < -2) else x for x in coords]
            v_screen = Matrix([coords]) * self.renderer.projection.to_screen_matrix
            screen_coords = (v_screen.matrix[0][0], v_screen.matrix[0][1])
            proj_vertices.append(screen_coords)

        for face in self.faces:
            polygon = [proj_vertices[i] for i in face]
            if self.any_func_nested(polygon, self.renderer.H_WIDTH, self.renderer.H_HEIGHT):
                continue

            i1, i2, i3 = face
            v1_cam = cam_vertices[i1].matrix[0]
            v2_cam = cam_vertices[i2].matrix[0]
            v3_cam = cam_vertices[i3].matrix[0]
            avg_depth = (v1_cam[2] + v2_cam[2] + v3_cam[2]) / 3.0

            v1_world = self.vertices[i1].matrix[0][:3]
            v2_world = self.vertices[i2].matrix[0][:3]
            v3_world = self.vertices[i3].matrix[0][:3]
            AB = Vector([v2_world[j] - v1_world[j] for j in range(3)])
            AC = Vector([v3_world[j] - v1_world[j] for j in range(3)])
            normal = AB.cross(AC)

            camera_forward = Vector(self.renderer.camera.forward.matrix[0][:3])
            dot = normal * camera_forward
            
            if self.one_side_polygons:
                if dot > 0:
                    continue

            norm_length = math.sqrt(sum(n * n for n in normal.vector))
            if norm_length == 0:
                continue
            norm_unit = [n / norm_length for n in normal.vector]
            light_unit = Vector(self.renderer.color_vectror.normalize()).vector
            brightness = (norm_unit[0] * light_unit[0] +
                          norm_unit[1] * light_unit[1] +
                          norm_unit[2] * light_unit[2])
            if brightness < 0:
                brightness = 0
            if brightness < 0.05:
                brightness = 0.05
            
            if not self.one_side_polygons:
                norm_unit_2 = [-x for x in norm_unit]
                brightness_2 = (norm_unit_2[0] * light_unit[0] +
                          norm_unit_2[1] * light_unit[1] +
                          norm_unit_2[2] * light_unit[2])
                
                if brightness_2 < 0:
                    brightness_2 = 0
                if brightness_2 < 0.05:
                    brightness_2 = 0.05
                
                brightness = max(brightness, brightness_2)

            intensity = int(brightness * 255)
            color = (intensity, 0, 0) if self.color_sensetivity else self.default_color

            polygon = [proj_vertices[i1], proj_vertices[i2], proj_vertices[i3]]
            faces_list.append((avg_depth, polygon, color))
        return faces_list

    def translate(self, pos):
        self.vertices = [vertex * translate(pos) for vertex in self.vertices]
    
    def scale(self, scale_factor):
        self.vertices = [vertex * scale(scale_factor) for vertex in self.vertices]

    def rotate_x(self, angle):
        self.vertices = [vertex * rotate_x(angle) for vertex in self.vertices]

    def rotate_y(self, angle):
        self.vertices = [vertex * rotate_y(angle) for vertex in self.vertices]

    def rotate_z(self, angle):
        self.vertices = [vertex * rotate_z(angle) for vertex in self.vertices]


class Cube(Object3D):
    def __init__(self, renderer, size, color_sensetivity=True, default_color=(255, 0, 0)):
        h_size = size / 2
        vertices = [
            Matrix([[h_size, h_size, h_size, 1]]),
            Matrix([[h_size, h_size, -h_size, 1]]),
            Matrix([[h_size, -h_size, h_size, 1]]),
            Matrix([[h_size, -h_size, -h_size, 1]]),
            Matrix([[-h_size, h_size, h_size, 1]]),
            Matrix([[-h_size, h_size, -h_size, 1]]),
            Matrix([[-h_size, -h_size, h_size, 1]]),
            Matrix([[-h_size, -h_size, -h_size, 1]]),
        ]

        faces = [
            (1, 0, 2),
            (1, 2, 3),
            (0, 5, 4),
            (0, 1, 5),
            (0, 4, 2),
            (2, 4, 6),
            (7, 6, 4),
            (4, 5, 7),
            (3, 6, 7),
            (3, 2, 6),
            (1, 7, 5),
            (1, 3, 7),
        ]

        super().__init__(renderer, vertices, faces, color_sensetivity, default_color)


class Octaeder(Object3D):
    def __init__(self, renderer, size, color_sensetivity=True, default_color=(255, 0, 0)):
        h_size = size / 2
        
        vertices = [Matrix([[h_size, 0, 0, 1]]), 
                         Matrix([[0, h_size, 0, 1]]), 
                         Matrix([[0, 0, h_size, 1]]), 
                         Matrix([[-h_size, 0, 0, 1]]), 
                         Matrix([[0, -h_size, 0, 1]]), 
                         Matrix([[0, 0, -h_size, 1]]), 
                        ]
        faces = [
                 (0, 1, 2), 
                 (2, 1, 3), 
                 (2, 3, 4), 
                 (0, 2, 4),
                 (5, 0, 4), 
                 (1, 0, 5), 
                 (3, 1, 5), 
                 (4, 3, 5)
                     ]

        super().__init__(renderer, vertices, faces, color_sensetivity, default_color)

class Sphere(Object3D):
    def __init__(self, renderer, size, subdivisions, color_sensetivity=True, default_color=(255, 0, 0)):
        
        
        radius = size / 2.0

        vertices = [[radius, 0, 0, 1], 
                    [0, radius, 0, 1], 
                    [0, 0, radius, 1], 
                    [-radius, 0, 0, 1], 
                    [0, -radius, 0, 1], 
                    [0, 0, -radius, 1], 
                ]
        
        faces = [
                 (0, 1, 2), 
                 (2, 1, 3), 
                 (2, 3, 4), 
                 (0, 2, 4),
                 (5, 0, 4), 
                 (1, 0, 5), 
                 (3, 1, 5), 
                 (4, 3, 5)
                     ]

        midpoint_cache = {}
        def get_midpoint(i1, i2):
            key = tuple(sorted((i1, i2)))
            if key in midpoint_cache:
                return midpoint_cache[key]
            v1 = vertices[i1]
            v2 = vertices[i2]

            mid = [ (v1[j] + v2[j]) / 2.0 for j in range(3) ]
            
            length = math.sqrt(sum(mid[j] * mid[j] for j in range(3)))
            mid = [ (mid[j] / length) * radius for j in range(3) ]
            vertices.append(mid)
            index = len(vertices) - 1
            midpoint_cache[key] = index
            return index

        for _ in range(subdivisions):
            new_faces = []
            midpoint_cache.clear()
            for tri in faces:
                i0, i1, i2 = tri
                a = get_midpoint(i0, i1)
                b = get_midpoint(i1, i2)
                c = get_midpoint(i2, i0)
                new_faces.extend([
                    (i0, a, c),
                    (i1, b, a),
                    (i2, c, b),
                    (a, b, c)
                ])
            faces = new_faces

        matrix_vertices = [Matrix([v + [1]]) for v in vertices]

        super().__init__(renderer, matrix_vertices, faces, color_sensetivity, default_color)

class Origin(Object3D):
    def __init__(self, renderer, size = 1, color_sensetivity=False, default_color=(255, 0, 0)):
        
        inner_cube_size = 0.1
        a, b = size, inner_cube_size

        vertices = [
            Matrix([[a, b, b, 1]]),
            Matrix([[a, b, 0, 1]]),
            Matrix([[a, 0, b, 1]]),
            Matrix([[a, 0, 0, 1]]),
            Matrix([[b, b, b, 1]]),
            Matrix([[b, b, 0, 1]]),
            Matrix([[b, 0, b, 1]]),
            Matrix([[b, 0, 0, 1]]),
            
            Matrix([[b, a, b, 1]]),
            Matrix([[b, a, 0, 1]]),
            Matrix([[0, a, b, 1]]),
            Matrix([[0, a, 0, 1]]),
            Matrix([[0, b, b, 1]]),
            Matrix([[0, b, 0, 1]]),

            Matrix([[b, b, a, 1]]),
            Matrix([[b, 0, a, 1]]),
            Matrix([[0, b, a, 1]]),
            Matrix([[0, 0, a, 1]]),
            Matrix([[0, 0, b, 1]])
        ]

        faces = [
            (1, 0, 2),
            (1, 2, 3),
            (0, 5, 4),
            (0, 1, 5),
            (0, 4, 2),
            (2, 4, 6),
            (7, 6, 4),
            (4, 5, 7),
            (3, 6, 7),
            (3, 2, 6),
            (1, 7, 5),
            (1, 3, 7),

            (9, 8, 4),
            (9, 4, 5),
            (8, 11, 10),
            (8, 9, 11),
            (8, 10, 4),
            (4, 10, 12),
            (13, 12, 10),
            (10, 11, 13),
            (5, 12, 13),
            (5, 4, 12),
            (9, 13, 11),
            (9, 5, 13),

            (4, 14, 15),
            (4, 15, 6),
            (14, 12, 16),
            (14, 4, 12),
            (14, 16, 15),
            (15, 16, 17),
            (18, 17, 16),
            (16, 12, 18),
            (6, 17, 18),
            (6, 15, 17),
            (4, 18, 12),
            (4, 6, 18),
        ]
        
        
        super().__init__(renderer, vertices, faces, color_sensetivity, default_color)

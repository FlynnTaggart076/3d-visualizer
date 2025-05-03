import pygame as pg
from matrix_functions import *


class Camera:
    def __init__(self, renderer, position):
        self.renderer = renderer
        self.position = Matrix([[*position, 1.0]])
        
        self.forward = Matrix([[0, 0, 1, 1]])
        self.up = Matrix([[0, 1, 0, 1]])
        self.right = Matrix([[1, 0, 0, 1]])

        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (self.renderer.HEIGHT / self.renderer.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100

        self.yaw = 0.0
        self.pitch = 0.0

        self.moving_speed = 0.1
        self.rotation_speed_keys = 0.015
        self.rotation_speed_mouse = 0.001

    def control(self):
        keys = pg.key.get_pressed()
        
        moving_speed = self.moving_speed
        if keys[pg.K_LCTRL]:
            moving_speed = self.moving_speed * 5

        if keys[pg.K_w]:
            self.position = self.position + self.forward * moving_speed
        if keys[pg.K_s]:
            self.position = self.position - self.forward * moving_speed
        if keys[pg.K_a]:
            self.position = self.position - self.right * moving_speed
        if keys[pg.K_d]:
            self.position = self.position + self.right * moving_speed 
        if keys[pg.K_LSHIFT]:
            self.position = self.position - self.up * moving_speed
        if keys[pg.K_SPACE]:
            self.position = self.position + self.up * moving_speed

        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx != 0:
            self.camera_yaw(mouse_dx * self.rotation_speed_mouse)
        if mouse_dy != 0:
            self.camera_pitch(mouse_dy * self.rotation_speed_mouse)

    
    def camera_yaw(self, angle):
        self.yaw += angle
    
    def camera_pitch(self, angle):
        self.pitch += angle
        self.pitch = max(-math.pi / 2, self.pitch)
        self.pitch = min(math.pi / 2, self.pitch)
    
    def axiiIdentity(self):
        self.forward = Matrix([[0, 0, 1, 1]])
        self.up = Matrix([[0, 1, 0, 1]])
        self.right = Matrix([[1, 0, 0, 1]])

    def camera_update_axii(self):
        rotate = rotate_x(self.pitch) * rotate_y(self.yaw)
        self.axiiIdentity()
        self.forward = self.forward * rotate
        self.right = self.right * rotate
        self.up = self.up * rotate

    def translate_matrix(self):
        x, y, z, w = self.position.matrix[0]
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    def rotate_matrix(self):
        rx, ry, rz, w = self.right.matrix[0]
        ux, uy, uz, w = self.up.matrix[0]
        fx, fy, fz, w = self.forward.matrix[0]
        return Matrix([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() * self.rotate_matrix()
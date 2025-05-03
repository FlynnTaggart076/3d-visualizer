from object_3d import *

class LabObjectParams():
    def __init__(self, a, b, a_step, b_step, u_range, v_range, uv_subdivs, x_f, y_f, z_f):
        self.a = a
        self.b = b
        self.a_step = a_step
        self.b_step = b_step
        self.u_range = u_range
        self.v_range = v_range
        self.uv_subdivs = uv_subdivs
        
        self.x_f = x_f
        self.y_f = y_f
        self.z_f = z_f

class LabObject(Object3D):
    def __init__(self, renderer, params : LabObjectParams, one_side_polygons=False, color_sensetivity=True, default_color=...):
        self.params = params
        
        vertices, faces = self.calculate_geometry(params)
        super().__init__(renderer, vertices, faces, one_side_polygons, color_sensetivity, default_color)

    def change_ab_params(self, da, db):
        self.params.a += self.params.a_step * da
        self.params.b += self.params.b_step * db

        self.vertices, self.faces = self.calculate_geometry(self.params)

    def calculate_geometry(self, params):
        u_min, u_max = params.u_range
        v_min, v_max = params.v_range
        n_u, n_v = params.uv_subdivs
        a, b = params.a, params.b

        du = (u_max - u_min) / n_u
        dv = (v_max - v_min) / n_v

        grid = []
        for i in range(n_u + 1):
            u = u_min + i * du
            row = []
            for j in range(n_v + 1):
                v = v_min + j * dv
                x = self.params.x_f(a, b, u, v)
                y = self.params.y_f(a, b, u, v)
                z = self.params.z_f(a, b, u, v)
                row.append([x, y, z, 1])
            grid.append(row)

        vertices = []
        index_map = {}
        for i in range(n_u + 1):
            for j in range(n_v + 1):
                idx = len(vertices)
                vertices.append(grid[i][j])
                index_map[(i, j)] = idx

        faces = []
        for i in range(n_u):
            for j in range(n_v):
                i0 = index_map[(i, j)]
                i1 = index_map[(i + 1, j)]
                i2 = index_map[(i + 1, j + 1)]
                i3 = index_map[(i, j + 1)]
                faces.append((i0, i1, i2))
                faces.append((i0, i2, i3))

        ref = [0, 0, 0]
        for v in vertices:
            ref[0] += v[0]
            ref[1] += v[1]
            ref[2] += v[2]
        num = len(vertices)
        ref = [x / num for x in ref]

        fixed_faces = []
        for face in faces:
            i0, i1, i2 = face
            p0 = vertices[i0][:3]
            p1 = vertices[i1][:3]
            p2 = vertices[i2][:3]

            edge1 = [p1[k] - p0[k] for k in range(3)]
            edge2 = [p2[k] - p0[k] for k in range(3)]

            normal = [
                edge1[1]*edge2[2] - edge1[2]*edge2[1],
                edge1[2]*edge2[0] - edge1[0]*edge2[2],
                edge1[0]*edge2[1] - edge1[1]*edge2[0]
            ]

            centroid = [(p0[k] + p1[k] + p2[k]) / 3.0 for k in range(3)]
            
            dir_vec = [centroid[k] - ref[k] for k in range(3)]
            dot = sum(normal[k] * dir_vec[k] for k in range(3))
            if dot < 0:
                fixed_faces.append((i0, i2, i1))
            else:
                fixed_faces.append(face)

        matrix_vertices = [Matrix([v]) for v in vertices]

        return matrix_vertices, fixed_faces
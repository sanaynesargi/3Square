#!/usr/bin/env python3
"""Generate two STL files for the L-Shape Visibility model:
1. cube.stl   — Q1 region, a solid 1×1×1 cube
2. curved.stl — Q2 region, with curved top from visibility formula
"""

import struct
import numpy as np

# --- Visibility formula (from index.html) ---

def vis_q2(x, y):
    """Visibility into Q3 from point (x,y) in Q2: x∈[1,2], y∈[0,1]."""
    eps = 1e-6
    x = np.clip(x, 1 + eps, 2 - eps)
    y = np.clip(y, eps, 1 - eps)
    s = x + y
    return np.where(
        s > 2,
        (1 - y) / (2 * (x - 1)),
        (3 - x - 2 * y) / (2 * (1 - y)),
    )

def height_q2(x, y):
    """Total visibility height for Q2 point. x∈[1,2], y∈[0,1]."""
    return (2 + vis_q2(x, y)) / 3


# --- Binary STL writer ---

def write_stl(filename, triangles):
    """Write binary STL. triangles: Nx3x3 array of vertex coords."""
    n = len(triangles)
    with open(filename, "wb") as f:
        f.write(b"\0" * 80)  # header
        f.write(struct.pack("<I", n))
        for tri in triangles:
            v0, v1, v2 = tri
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = np.cross(edge1, edge2)
            norm = np.linalg.norm(normal)
            if norm > 0:
                normal /= norm
            f.write(struct.pack("<3f", *normal))
            f.write(struct.pack("<3f", *v0))
            f.write(struct.pack("<3f", *v1))
            f.write(struct.pack("<3f", *v2))
            f.write(struct.pack("<H", 0))  # attribute byte count
    print(f"  {filename}: {n} triangles, {80 + 4 + n * 50} bytes")


# --- 1. Cube (Q1) ---

def make_cube():
    """Unit cube [0,1]^3."""
    tris = []

    def quad(a, b, c, d):
        tris.append([a, b, c])
        tris.append([a, c, d])

    # vertices
    v = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],  # top
    ], dtype=np.float32)

    quad(v[0], v[3], v[2], v[1])  # bottom (z=0) outward-facing
    quad(v[4], v[5], v[6], v[7])  # top (z=1)
    quad(v[0], v[1], v[5], v[4])  # front (y=0)
    quad(v[2], v[3], v[7], v[6])  # back (y=1)
    quad(v[0], v[4], v[7], v[3])  # left (x=0)
    quad(v[1], v[2], v[6], v[5])  # right (x=1)

    return np.array(tris, dtype=np.float32)


# --- 2. Curved part (Q2) ---

def make_curved(res=100):
    """Q2 region with curved top surface.
    STL coords: x∈[0,1], y∈[0,1], z = height from visibility.
    Math coords: x_math = x+1 ∈ [1,2], y_math = y ∈ [0,1].
    """
    tris = []

    # Grid of x,y values
    xs = np.linspace(0, 1, res + 1)
    ys = np.linspace(0, 1, res + 1)
    X, Y = np.meshgrid(xs, ys)

    # Heights: map to math coords [1,2]×[0,1]
    Z = height_q2(X + 1, Y).astype(np.float32)

    # --- Top surface ---
    for j in range(res):
        for i in range(res):
            x0, x1 = xs[i], xs[i + 1]
            y0, y1 = ys[j], ys[j + 1]
            z00 = Z[j, i]
            z10 = Z[j, i + 1]
            z01 = Z[j + 1, i]
            z11 = Z[j + 1, i + 1]
            tris.append([[x0, y0, z00], [x1, y0, z10], [x1, y1, z11]])
            tris.append([[x0, y0, z00], [x1, y1, z11], [x0, y1, z01]])

    # --- Bottom surface (z=0) ---
    for j in range(res):
        for i in range(res):
            x0, x1 = xs[i], xs[i + 1]
            y0, y1 = ys[j], ys[j + 1]
            tris.append([[x0, y0, 0], [x1, y1, 0], [x1, y0, 0]])
            tris.append([[x0, y0, 0], [x0, y1, 0], [x1, y1, 0]])

    # --- Side walls ---
    # Front wall: y=0, x varies
    for i in range(res):
        x0, x1 = xs[i], xs[i + 1]
        z0, z1 = Z[0, i], Z[0, i + 1]
        tris.append([[x0, 0, 0], [x1, 0, 0], [x1, 0, z1]])
        tris.append([[x0, 0, 0], [x1, 0, z1], [x0, 0, z0]])

    # Back wall: y=1, x varies
    for i in range(res):
        x0, x1 = xs[i], xs[i + 1]
        z0, z1 = Z[res, i], Z[res, i + 1]
        tris.append([[x0, 1, 0], [x1, 1, z1], [x1, 1, 0]])
        tris.append([[x0, 1, 0], [x0, 1, z0], [x1, 1, z1]])

    # Left wall: x=0, y varies
    for j in range(res):
        y0, y1 = ys[j], ys[j + 1]
        z0, z1 = Z[j, 0], Z[j + 1, 0]
        tris.append([[0, y0, 0], [0, y1, z1], [0, y1, 0]])
        tris.append([[0, y0, 0], [0, y0, z0], [0, y1, z1]])

    # Right wall: x=1, y varies
    for j in range(res):
        y0, y1 = ys[j], ys[j + 1]
        z0, z1 = Z[j, res], Z[j + 1, res]
        tris.append([[1, y0, 0], [1, y1, 0], [1, y1, z1]])
        tris.append([[1, y0, 0], [1, y1, z1], [1, y0, z0]])

    return np.array(tris, dtype=np.float32)


# --- Main ---

if __name__ == "__main__":
    print("Generating STL files...")

    print("1. Cube (Q1):")
    cube_tris = make_cube()
    write_stl("cube.stl", cube_tris)

    print("2. Curved surface (Q2):")
    curved_tris = make_curved(res=100)
    write_stl("curved.stl", curved_tris)

    print("Done!")

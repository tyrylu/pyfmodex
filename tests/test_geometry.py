def test_add_polygon(geometry):
    idx = geometry.add_polygon(0.5, 0.5, False, (0,0,0), (1,1,0), (1,0,0))
    assert idx == 0

def test_active(geometry):
    assert geometry.active
    geometry.active = False
    assert not geometry.active

def test_max_polygons(geometry):
    assert geometry.max_polygons == 42

def test_max_vertices(geometry):
    assert geometry.max_vertices == 420

def test_num_polygons(geometry):
    assert geometry.num_polygons == 0

def test_polygon(geometry):
    geometry.add_polygon(0.5, 0.5, False, (0,0,0), (1,1,0), (1,0,0))
    poly = geometry.get_polygon(0)
    assert poly.direct_occlusion == 0.5
    poly.direct_occlusion = 1.0
    assert poly.direct_occlusion == 1.0
    assert poly.reverb_occlusion == 0.5
    poly.reverb_occlusion = 1.0
    assert not poly.double_sided
    poly.double_sided = True
    assert poly.double_sided
    assert poly.reverb_occlusion == 1.0
    assert poly.num_vertices == 3
    assert poly.get_vertex(0) == [0.0, 0.0, 0.0]
    poly.set_vertex(0, [0.0, 0.0, 0.25])
    assert poly.get_vertex(0) == [0.0, 0.0, 0.25]

def test_position(geometry):
    assert geometry.position == [0.0, 0.0, 0.0]
    new_pos = [1.0, 2.0, 3.0]
    geometry.position = new_pos
    assert geometry.position == new_pos

def test_rotation(geometry):
    assert geometry.forward_rotation == [0.0, 0.0, 1.0]
    assert geometry.up_rotation == [0.0, 1.0, 0.0]
    new_fwd_rot = [1.0, 0.0, 0.0]
    new_up_rot = [0.0, 0.0, 1.0]
    geometry.forward_rotation = new_fwd_rot
    assert geometry.forward_rotation == new_fwd_rot
    geometry.up_rotation = new_up_rot
    assert geometry.up_rotation == new_up_rot

def test_scale(geometry):
    assert geometry.scale == [1.0, 1.0, 1.0]
    new_scale = [2.0, 1.0, 3.5]
    geometry.scale = new_scale
    assert geometry.scale == new_scale

def test_release(geometry):
    geometry.release()

def test_save_and_load(initialized_system, geometry):
    data = geometry.save()
    geom2 = initialized_system.load_geometry(data)
    assert geom2.num_polygons == 0


class Drawer(object):

    image = None
    _drawer = None
    
    @property
    def drawer(self):
        if self._drawer is None:
            self.drawer_new()
        return self._drawer
    
    def close(self):
        self._drawer = None
        return self


# gimp Drawer wrapper
class GimpDrawer(Drawer):
    
    def __init__(self, image):
        self.image = image
        self._drawer = None
    
    def drawer_new(self, size=None, name='unnamed'
            , opacity=100, mode=NORMAL_MODE, visible=True, linked=False
            , position=0, parent=None
            , offset=None):
        image = self.image
        width, height = (None, None) if size is None else size
        if width is None: width = image.width
        if height is None: height = image.height
        self._drawer = pdb.gimp_layer_new(image, image.width, image.height, RGBA_IMAGE, name, opacity, mode)
        pdb.gimp_image_insert_layer(image, self._drawer, parent, position)
        self._drawer.visible = visible
        self._drawer.linked = linked
        if offset is not None:
            pdb.gimp_layer_set_offsets(self._drawer, *offset)
        return self._drawer
    
    def draw_polygon(self, pd, outline=None, weight=1.0, fill=None):
        image, imdraw = self.image, self.drawer
        l_pd = len(pd)
        pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, l_pd, pd)
        if pdb.gimp_selection_is_empty(image): return False
        if fill:
            if hasattr(fill, '__len__'):
                pdb.gimp_context_set_background(fill)
            pdb.gimp_edit_bucket_fill(imdraw, BG_BUCKET_FILL, 0, 100, 15, False, 0, 0)
        if outline:
            pdb.gimp_selection_grow(image, weight)
            pdb.gimp_image_select_polygon(image, CHANNEL_OP_SUBTRACT, l_pd, pd)
            if not pdb.gimp_selection_is_empty(image):
                if hasattr(outline, '__len__'):
                    pdb.gimp_context_set_foreground(outline)
                pdb.gimp_edit_bucket_fill(imdraw, FG_BUCKET_FILL, 0, 100, 15, False, 0, 0)
        return True


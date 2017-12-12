
import bpy

class Interface(bpy.types.Panel):
    """
    Global Batch Blender Interface. Handles the separate UI
    definitions of all the submodules based on the session page.
    Also provides custom functions for display props, ops and labels.
    """

    bl_label = "Azure Batch Rendering"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"


    def label(self, label, row, align=None, icon=None, active=True):
        """
        Display a text label.

        :Args:
            - label (str): The text to display.
            - row (:class:`bpy.types.UILayout`): The layout component to
              add the label to.

        :Kwargs:
            - align (str): If set, will align the label according to the
              Blender enum: {'LEFT', 'RIGHT', 'CENTER', 'EXPAND'}
            - icon: (str): If set, will display an icon with the label, from
              the Blender icon list.
            - active (bool): If true, the UI label will be enabled, else it
              will be greyed out. Note that due to how this works in Blender,
              this attribute will be applied to the whole UILayout component
              not just this label.
        """
        if align:
            row.alignment = align

        if icon:
            row.label(text=label, icon=icon)

        else:
            row.label(text=label)
        row.enabled = active


    def prop(self, data, prop, row, label="",align=None, active=True,
             **kwargs):
        """
        Display a Blender property.

        :Args:
            - data (Blender context): The context of which the property is
              an attribute.
            - prop (str): The property (attribute name) to be displayed.
            - row (:class:`bpy.types.UILayout`): The layout component to
              dispaly the property on.

        :Kwargs:
            - label (str): Any test to accompany the property. Default is "".
            - align (str): If set, will align the label according to the
              Blender enum: {'LEFT', 'RIGHT', 'CENTER', 'EXPAND'}
            - active (bool): If true, the UI prop will be enabled, else it
              will be greyed out. Note that due to how this works in Blender,
              this attribute will be applied to the whole UILayout component
              not just this property.
        """
        if align:
            row.alignment = align

        if label is not None:
            row.prop(data, prop, text=label, **kwargs)

        else:
            row.prop(data, prop, **kwargs)

        row.enabled = active


    def operator(self, op, label, row, icon="NONE", align=None, active=True):
        """
        Display a registered Blender operator as a button.

        :Args:
            - op (bpy.types.Operator): A Blender operator to display a
              button for.
            - label (str): The text to display on the button.
            - row (:class:`bpy.types.UILayout`): The layout component to
              dispaly the button on.

        :Kwargs:
            - icon: (str): If set, will display an icon on the button, from
              the Blender icon list.
            - align (str): If set, will align the button according to the
              Blender enum: {'LEFT', 'RIGHT', 'CENTER', 'EXPAND'}
            - active (bool): If true, the UI button will be enabled, else it
              will be greyed out. Note that due to how this works in Blender,
              this attribute will be applied to the whole UILayout component
              not just this button.
        """
        if align:
            row.alignment = align

        row.operator("batch_" + op, text=label, icon=icon)
        row.enabled = active


    def draw(self, context):
        """
        The global draw method. This is called every time Blender's UI
        is refreshed.
        Which page of the addon is display is set by the Batch session
        context. If the requested page is not recognized, the error page
        is displayed.

        :Args:
            - context (bpy.types.Context): The current Blender runtime context.
        """
        if hasattr(context.scene, "batch_error"):
            self.load_failed()
            return

        session = context.scene.batch_session

        if session.page in session.pages:
            session.display(self, self.layout)
        
        else:
            session.log.error("draw() :: Can't load page: {0}. No definition found".format(session.page))

            session.page = "ERROR"
            session.display(self, self.layout)


    def load_failed(self):
        """
        Display error page if the addon failed to load.

        """
        sublayout = self.layout.box()
        self.label("Plugin failed to load correctly", sublayout.row(align=True), "CENTER")
        self.label("Please see console for details.", sublayout.row(align=True), "CENTER")
        self.label("", sublayout)


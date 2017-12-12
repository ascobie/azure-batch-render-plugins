
import bpy

def home(ui, layout):
    """
    Display home page.

    :Args:
        - ui (blender :class:`.Interface`): The instance of the Interface
            panel class.
        - layout (blender :class:`bpy.types.UILayout`): The layout object,
            derived from the Interface panel. Used for creating ui
            components.

    """
    col = layout.column()
    ui.operator("shared.submit_job", "Submit Job", col)
    ui.operator("shared.monitor_jobs", "Monitor Jobs", col)
    ui.operator("shared.monitor_pools", "Monitor Pools", col)
    ui.operator("shared.download_renders", "Download Renders", col)
    ui.label("", layout)

def error(ui, layout):
    """
    Display error page.

    :Args:
        - ui (blender :class:`.Interface`): The instance of the Interface
            panel class.
        - layout (blender :class:`bpy.types.UILayout`): The layout object,
            derived from the Interface panel. Used for creating ui
            components.

    """
    sublayout = layout.box()
    ui.label("An error occurred", sublayout.row(align=True), "CENTER")
    ui.label("Please see console for details.", sublayout.row(align=True), "CENTER")
    ui.operator("shared.home", "Return Home", sublayout)

    ui.label("", sublayout)

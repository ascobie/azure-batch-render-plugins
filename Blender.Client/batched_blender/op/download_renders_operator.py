import bpy
import logging
import webbrowser

class DownloadRendersOperator(bpy.types.Operator):
    bl_idname = "batch_shared.download_renders"
    bl_label = "DownloadRendersOperator"

    def __init__(self):
        self.log = logging.getLogger('batched_blender')

    def execute(self, context):
        self.log.debug("DownloadRendersOperator.execute")
        # webbrowser.open("ms-batchlabs://route/data", 1, True)

        return {"FINISHED"}

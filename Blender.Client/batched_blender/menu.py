
import bpy

class BatchLabsBlenderMenu(bpy.types.Menu):
    """
    BatchLabs menu options for Blender.
    Displays a menu item under the info > render menu.
    Azure Batch Rendering
        > Submit Job
        > Download Renders
        > Monitor Pools
        > Monitor Jobs
    """
    bl_label = "Azure Batch Rendering"

    def draw(self, context):
        layout = self.layout
        self.layout.operator("batch_shared.submit_job", text="Submit Job")
        self.layout.operator("batch_shared.download_renders", text="Download Renders")
        self.layout.operator("batch_shared.monitor_pools", text="Monitor Pools")
        self.layout.operator("batch_shared.monitor_jobs", text="Monitor Jobs")

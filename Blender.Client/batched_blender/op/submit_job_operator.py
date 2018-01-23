import bpy
import webbrowser

class SubmitJobOperator(bpy.types.Operator):
    bl_idname = "batch_shared.submit_job"
    bl_label = "SubmitJobOperator"
    job_type = bpy.props.StringProperty()

    def execute(self, context):
        print("job_type:",self.job_type)
        self.report({"INFO"}, "%s"%(self.job_type))
        return {"FINISHED"}

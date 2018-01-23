
import bpy

class BatchOps(object):
    """
    Static class for registering operators and executing them in a
    error-safe way.
    """

    @staticmethod
    def session(func, *args, **kwargs):
        """
        Execute an operator function.
        Can be invoke, execute, modal or a thread function.

        :Args:
            - func (function): The function to be executed along with
              any args and kwargs.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
            - If an exception is raised, returns {'CANCELLED'}.
        """
        session = bpy.context.scene.batch_session

        try:
            return func(*args, **kwargs)

        except Exception as exp:
            session.log.error("Error occurred: {0}".format(exp))
            session.redraw()

            return {'CANCELLED'}


    @staticmethod
    def register(name, label, execute=None, modal=None, invoke=None, **kwargs):
        """
        Register a custom operator.

        :Args:
            - name (str): The id name of the operator (bl_idname).
            - label (str): The description of the operator (bl_label).

        :Kwargs:
            - execute (func): The execute function if applicable.
            - modal (func): The modal function if applicable.
            - invoke (func): The invoke function if applicable.
            - Any additional attributes or functions to be added to the class.

        :Returns:
            - The ID name of the registered operator with the
              prefix ``batch_``.

        """
        name = "batch_" + str(name)
        op_spec = {"bl_idname": name, "bl_label": label}
        op_spec["job_type"] = ""

        if execute:
            def op_execute(self, context):
                return BatchOps.session(execute, self, context)

            op_spec["execute"] = op_execute

        if modal:
            def op_modal(self, context, event):
                return BatchOps.session(modal, self, context, event)

            op_spec["modal"] = op_modal

        if invoke:
            def op_invoke(self, context, event):
                return BatchOps.session(invoke, self, context, event)

            op_spec["invoke"] = op_invoke

        op_spec.update(kwargs)
        new_op = type("BatchOp", (bpy.types.Operator, ), op_spec)
        bpy.utils.register_class(new_op)

        return name

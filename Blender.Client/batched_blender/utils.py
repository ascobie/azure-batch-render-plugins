
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
            session.page = "ERROR"
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


class BatchAsset(object):

    def __init__(self, file_path, client):        
        path = os.path.realpath(bpy.path.abspath(file_path))
        self.path = os.path.normpath(path)
        self.name = os.path.basename(self.path)
        
        self._client = client
        self._exists = os.path.exists(self.path)
        self.lastmodified = datetime.datetime.fromtimestamp(os.path.getmtime(self.path)) if self._exists else None
        self.checksum = self.get_checksum() if self._exists else None

    def get_checksum(self):
        """Generate md5 checksum for file.
        :Returns:
            - The md5 checksum of the file (bytes).
        """
        block_size = 128
        hasher = hashlib.md5()
        try:
            with open(self.path, 'rb') as user_file:
                while True:
                    file_block = user_file.read(block_size)
                    if not file_block:
                        break
                    hasher.update(file_block)
            return hasher.hexdigest()

        except (TypeError, EnvironmentError) as exp:
            bpy.context.scene.batch_session.log.info("Can't get checksum: {0}".format(exp))
            return None

    def get_last_modified(self):
        if self._exists:
            mod = os.path.getmtime(self.path)
            return datetime.datetime.fromtimestamp(mod)

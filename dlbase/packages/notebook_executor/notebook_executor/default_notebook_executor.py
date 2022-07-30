"""Base papermill wrapper."""
import papermill as pm
import papermill.iorw as pio

class DefaultNotebookExecutor():
  """DefaultNotebookExecutor wraps a papermill execution."""
  def __init__(self, nb_in, nb_out, nb_params, nb_params_file, kernel_name):
    self.input = nb_in
    self.output = nb_out
    self.params = {}

    if nb_params:
      self.params.update(nb_params)

    if nb_params_file:
      yaml_params = pio.read_yaml_file(nb_params_file)
      self.params.update(yaml_params)

    self.kernel_name = None
    if kernel_name:
      self.kernel_name = kernel_name

  def pre_execution(self):
    pass

  def execute(self):
    self.pre_execution()
    pm.execute_notebook(self.input, self.output,
                        parameters=self.params, kernel_name=self.kernel_name)
    self.post_execution()

  def post_execution(self):
    pass

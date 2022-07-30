"""CLI interface to papermill wrapper."""
import argparse
import notebook_executor

class StoreDictKeyPair(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    params_dict = {}
    for key_value in values.split(","):
      key,value = key_value.split("=")
      params_dict[key.strip()] = value.strip()
    setattr(namespace, self.dest, params_dict)


def _create_executor(input_nb, output_nb, parameters, parameters_file,
                     kernel_name):
  if input_nb.startswith("gs://"):
    return notebook_executor.GcsNotebookExecutor(
        nb_in=input_nb, nb_out=output_nb, nb_params=parameters,
        nb_params_file=parameters_file, kernel_name=kernel_name)
  return notebook_executor.DefaultNotebookExecutor(
      nb_in=input_nb, nb_out=output_nb, nb_params=parameters,
      nb_params_file=parameters_file, kernel_name=kernel_name)


def _get_input_arguments():
  """Argparse helper."""
  parser = argparse.ArgumentParser(description="Execute notebook.")
  parser.add_argument("--input-notebook", dest="input_notebook", required=True)
  parser.add_argument("--output-notebook", dest="output_notebook",
                      required=True)
  parser.add_argument("--parameters-file", dest="parameters_file",
                      required=False)
  parser.add_argument("--parameters", dest="parameters",
                      action=StoreDictKeyPair,
                      metavar="KEY1=VAL1,KEY2=VAL2...", required=False)
  parser.add_argument("--kernel-name", dest="kernel_name", required=False)
  return parser.parse_args()


def main():
  args = _get_input_arguments()

  input_notebook = args.input_notebook
  output_notebook = args.output_notebook
  parameters = args.parameters
  parameters_file = args.parameters_file
  kernel_name = args.kernel_name

  executor = _create_executor(input_notebook, output_notebook, parameters,
                              parameters_file, kernel_name)
  executor.execute()


if __name__ == "__main__":
  main()

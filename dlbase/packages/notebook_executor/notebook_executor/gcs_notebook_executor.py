"""GCS papermill wrapper"""
import subprocess

from notebook_executor import DefaultNotebookExecutor

# First normal reaction to the following code should be: why to call bash, all
# these can and should be done via the APIs! Since this is a valid reaction
# first version of this class indeed was via the API. These create two problems.
# First, looks like not all operations even possible to do via SDK, I have not
# found how to request list of versions of a blob in a simple way. Second
# problem, even for the part that does can be done with SDK it took ~150 more
# lines of code. Making code hard to read and more error prone.
CHECK_STAT = "gsutil stat {gcs_path}"
GET_LIST_OF_ACLS = "gsutil acl get {gcs_path} > /tmp/acls"
SET_ACLS_FOR_GCS_FILE = "gsutil acl set /tmp/acls {gcs_path}"
GET_LIST_OF_VERSIONS = "gsutil ls -a {gcs_path} > /tmp/versions"
UPLOAD_LIST_OF_VERSIONS = "gsutil cp /tmp/versions {gcs_path}_versions"


class GcsNotebookExecutor(DefaultNotebookExecutor):
  """GcsNotebookExecutor creates a papermill execution sourced from GCS."""
  def __init__(self, nb_in, nb_out, nb_params, nb_params_file, kernel_name):
    super().__init__(nb_in, nb_out, nb_params, nb_params_file, kernel_name)
    self.exists_prior = False

  def pre_execution(self):
    stat_result = _execute_shell(CHECK_STAT.format(gcs_path=self.output))
    if "No URLs matched" not in stat_result:
      _execute_shell(GET_LIST_OF_ACLS.format(gcs_path=self.output))
      self.exists_prior = True

  def post_execution(self):
    if self.exists_prior:
      _execute_shell(SET_ACLS_FOR_GCS_FILE.format(gcs_path=self.output))
      _execute_shell(GET_LIST_OF_VERSIONS.format(gcs_path=self.output))
      _execute_shell(UPLOAD_LIST_OF_VERSIONS.format(
          gcs_path=self.output))
      _execute_shell(SET_ACLS_FOR_GCS_FILE.format(
          gcs_path=f"{self.output}_versions"))

def _execute_shell(command):
  with subprocess.Popen(command, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
    output, _ = p.communicate()
  return output.decode('ascii').replace("\n", "")

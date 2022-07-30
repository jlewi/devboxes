"""IPython configuration file."""

# pylint: disable=undefined-variable
c.IPKernelApp.extensions = [
    'beatrix_jupyterlab',
    'google.cloud.bigquery',
    'sql'
]
c.InteractiveShellApp.matplotlib = 'inline'

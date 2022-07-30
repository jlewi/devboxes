package(default_visibility = ["//visibility:public"])

licenses(["unencumbered"])

py_library(
    name = "py_lib",
    srcs = [
        "gcs_utils.py",
        "datastore_utils.py"
    ],
    deps = [
      "//common:py_lib"
    ]
)

py_test(
    name = "datastore_utils_test",
    size = "small",
    srcs = ["datastore_utils_test.py"],
    deps = [":py_lib"],
)

test_suite(
    name = "all_tests",
    tests = [
        ":datastore_utils_test"
    ],
)

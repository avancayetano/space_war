import cx_Freeze

executables = [cx_Freeze.Executable("spacewar.py")]

cx_Freeze.setup(
    name="Spacewar",
    version="1.0",
    author="avan",
    description="hatdog",
    options={"build_exe": {"packages":["pygame", "json"],
                           "include_files":["TheComplex.mp3"]}},
    executables = executables
    )

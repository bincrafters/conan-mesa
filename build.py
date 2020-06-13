#!/usr/bin/env python

from bincrafters import build_template_default
from conans import tools
import os

if __name__ == "__main__":
    docker_entry_script = None
    if os.getenv("CONAN_GCC_VERSIONS") == "4.9":
        docker_entry_script = "conan install ninja/1.10.0@ --build ninja"

    builder = build_template_default.get_builder(pip_install=["Mako"], pure_c=False, docker_entry_script=docker_entry_script)
    builder.update_build_if(lambda build:\
        (build.settings['compiler'] == 'gcc' and tools.Version(build.settings['compiler.version']) < "6") or \
        (build.settings['compiler'] == 'clang' and tools.Version(build.settings['compiler.version']) < "6"),
        new_settings = {'compiler.cppstd': '11'})
    builder.run()

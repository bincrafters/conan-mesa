#!/usr/bin/env python

from bincrafters import build_template_default
from conans.client.build.cppstd_flags import cppstd_default
import os

if __name__ == "__main__":
    docker_entry_script = None
    if os.getenv("CONAN_GCC_VERSIONS") == "4.9":
        docker_entry_script = "conan install ninja/1.9.0@ --build ninja"

    builder = build_template_default.get_builder(pip_install=["Mako"], pure_c=False, docker_entry_script=docker_entry_script)
    builder.update_build_if(lambda build: cppstd_default(build.settings['compiler'], build.settings['compiler.version']).endswith('98'),
        new_settings = {'compiler.cppstd': '11'})
    builder.run()

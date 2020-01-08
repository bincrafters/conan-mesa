#!/usr/bin/env python

from bincrafters import build_template_default
from conans.client.build.cppstd_flags import cppstd_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pip_install=["Mako"], pure_c=False)
    builder.update_build_if(lambda build: cppstd_default(build.settings['compiler'], build.settings['compiler.version']).endswith('98'),
        new_settings = {'compiler.cppstd': '11'})
    builder.run()

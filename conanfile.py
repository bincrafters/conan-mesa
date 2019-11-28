from conans import ConanFile, Meson, tools
import os
import shutil


class LibnameConan(ConanFile):
    name = "mesa"
    description = "Keep it short"
    topics = ("conan", "mesa", "OpenGL")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    generators = "pkg_config"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {
        "shared": False,
        "fPIC": True,
        "libxcb:shared": True
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11",
        "expat/2.2.9",
        "libdrm/2.4.100@bincrafters/testing",
        "libx11/1.6.8@bincrafters/stable",
        "libxext/1.3.4@bincrafters/stable",
        "libxdamage/1.1.5@bincrafters/stable",
        "libxshmfence/1.3@bincrafters/stable",
        "libxxf86vm/1.1.4@bincrafters/stable"
    )

    def build_requirements(self):
        if not tools.which("meson"):
            self.build_requires("meson/0.52.0")
        if not tools.which('pkg-config'):
            self.build_requires('pkg-config_installer/0.29.2@bincrafters/stable')
        if not tools.which("bison"):
            self.build_requires("bison_installer/3.3.2@bincrafters/stable")
        if not tools.which("flex"):
            self.build_requires("flex_installer/2.6.4@bincrafters/stable")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)


    def _configure_meson(self):
        def _get_pc_files(package):
            if package in self.deps_cpp_info.deps:
                lib_path = self.deps_cpp_info[package].rootpath
                for dirpath, _, filenames in os.walk(lib_path):
                    for filename in filenames:
                        if filename.endswith('.pc'):
                            shutil.copyfile(os.path.join(dirpath, filename), filename)
                            tools.replace_prefix_in_pc_file(filename, lib_path)
                for dep in self.deps_cpp_info[package].public_deps:
                    _get_pc_files(dep)
        for p in ['libdrm', 'libx11', 'libxext', 'libxdamage', 'libxshmfence', 'libxxf86vm']:
            _get_pc_files(p)

        meson = Meson(self)
        meson.configure(
            defs={
                "llvm": "false",
                "gallium-drivers": "",
                "vulkan-drivers": "",
                "platforms": "x11"
            },
            source_folder=self._source_subfolder,
            build_folder=self._build_subfolder)
        return meson

    def build(self):
        meson = self._configure_meson()
        meson.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        meson = self._configure_meson()
        meson.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
	Extension(
		"StorageOrigin",
		["StorageOrigin.pyx"],
		extra_compile_args=["/O2"],
		extra_link_args=[],
	)
]

setup(
	name="StorageOrigin",
	ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
	zip_safe=False,
)

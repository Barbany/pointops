import glob
import os.path as osp

from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

this_dir = osp.dirname(osp.abspath(__file__))
_ext_src_root = osp.join("pointops", "_ext-src")
_ext_sources = glob.glob(
    osp.join(_ext_src_root, "src", "**", "*.cpp"), recursive=True
) + glob.glob(osp.join(_ext_src_root, "src", "**", "*.cu"), recursive=True)


requirements = ["torch>=1.4"]

setup(
    name="pointops",
    version="3.0.0",
    install_requires=requirements,
    packages=find_packages(),
    ext_modules=[
        CUDAExtension(
            name="pointops._ext",
            sources=_ext_sources,
            extra_compile_args={
                "cxx": ["-g"],
                "nvcc": ["-O2"],
            },
            include_dirs=[
                d
                for d in glob.glob(
                    osp.join(this_dir, _ext_src_root, "include", "**"), recursive=True
                )
                if osp.isdir(d)
            ],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)

# coding: utf-8
from setuptools import setup, find_packages
from distutils.core import Extension
import subprocess


def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}

    result = subprocess.check_output(['pkg-config', '--libs', '--cflags', packages[0]]).decode().strip()
    for token in result.split():
        if token[:2] in flag_map:
            kw.setdefault(flag_map[token[:2]], []).append(token[2:])
        else:  # throw others to extra_link_args
            kw.setdefault('extra_link_args', []).append(token)

    for key in kw.keys():  # remove duplicated
        kw[key] = list(set(kw[key]))

    return kw


ext_modules = [
    Extension(
        "xmmsclient.xmmsvalue", ["xmmsvalue.c"], **pkgconfig('xmms2-client')),
    Extension("xmmsclient.xmmsapi", ["xmmsapi.c"], **pkgconfig('xmms2-client'))
]

setup(
    name='xmmsclient',
    summary='Xmms2 native client',
    version='0.8.1',
    license='LGPL',
    maintainer=u'Loïc Faure-Lacroix',
    maintainer_email='lamerstar@gmail.com',
    packages=find_packages(),
    home_page='http://xmms2.org/wiki/Main_Page',
    ext_modules=ext_modules
)

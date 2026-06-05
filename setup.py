from setuptools import setup, find_packages

setup(
    name='maze',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'yt-dlp>=2023.0.0',
        'rich>=13.0.0',
    ],
    entry_points={
        'console_scripts': [
            'mz=maze.cli:main',
        ],
    },
    author='Maze',
    description='Universal CLI video downloader for YouTube, Instagram, and more',
    python_requires='>=3.8',
)

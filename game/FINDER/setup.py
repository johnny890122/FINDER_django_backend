from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext':build_ext},
    ext_modules = [
                    Extension('PrepareBatchGraph', sources = ['game/FINDER/PrepareBatchGraph.pyx','game/FINDER/src/lib/PrepareBatchGraph.cpp','game/FINDER/src/lib/graph.cpp','game/FINDER/src/lib/graph_struct.cpp',  'game/FINDER/src/lib/disjoint_set.cpp'], language='c++', extra_compile_args=['-std=c++11']),
                   Extension('graph', sources=['game/FINDER/graph.pyx', 'game/FINDER/src/lib/graph.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('mvc_env', sources=['game/FINDER/mvc_env.pyx', 'game/FINDER/src/lib/mvc_env.cpp', 'game/FINDER/src/lib/graph.cpp','game/FINDER/src/lib/disjoint_set.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('utils', sources=['game/FINDER/utils.pyx', 'game/FINDER/src/lib/utils.cpp', 'game/FINDER/src/lib/graph.cpp', 'game/FINDER/src/lib/graph_utils.cpp', 'game/FINDER/src/lib/disjoint_set.cpp', 'game/FINDER/src/lib/decrease_strategy.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('nstep_replay_mem', sources=['game/FINDER/nstep_replay_mem.pyx', 'game/FINDER/src/lib/nstep_replay_mem.cpp', 'game/FINDER/src/lib/graph.cpp', 'game/FINDER/src/lib/mvc_env.cpp', 'game/FINDER/src/lib/disjoint_set.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('nstep_replay_mem_prioritized',sources=['game/FINDER/nstep_replay_mem_prioritized.pyx', 'game/FINDER/src/lib/nstep_replay_mem_prioritized.cpp','game/FINDER/src/lib/graph.cpp', 'game/FINDER/src/lib/mvc_env.cpp', 'game/FINDER/src/lib/disjoint_set.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('graph_struct', sources=['game/FINDER/graph_struct.pyx', 'game/FINDER/src/lib/graph_struct.cpp'], language='c++',extra_compile_args=['-std=c++11']),
                    Extension('FINDER', sources = ['game/FINDER/FINDER.pyx'])
                   ])

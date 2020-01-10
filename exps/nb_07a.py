
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/07a_LSUV.ipynb

from exps.nb_07 import *

def get_batch(dl,run):
    run.xb,run.yb = next(iter(dl))
    for cb in run.cbs:cb.set_runner(run)
    run('begin_batch')
    return run.xb,run.yb

def find_modules(m,cond):
    if cond(m): return [m]
    return sum([find_modules(o,cond) for o in m.children()],[])

def is_lin_layer(l):
    lin_layers = (nn.Conv1d,nn.Conv2d,nn.Conv3d,nn.Linear,nn.ReLU)
    return is_instance(l,lin_layers)

def lsuv_module(m,xb):
    h = Hook(m,append_stat)

    while mdl(xb) is not None and abs(h.mean) > 1e-3: m.bias-=h.mean
    while mdl(xb) is not None and abs(h.std-1) >1e-3: m.weight.data/=h.std

    h.remove()
    return h.mean,h.std
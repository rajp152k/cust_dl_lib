
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/06_hooks.ipynb

def normalize_to(train,valid):
    m,s = train.mean(),train.std()
    return normalize(train,m,s),normalize(valid,m,s)

class Lambda(nn.Module):
    def __init__(self,func):
        super().__init__()
        self.func = func
    def forward(self,x): return self.func(x)

def flatten(x): return x.view(x.shape[0],-1)

class CudaCallback(Callback):
    def begin_fit(self):self.model.cuda()
    def begin_batch(self):
        self.run.xb = self.run.xb.cuda()
        self.run.yb = self.run.yb.cuda()

class BatchTransformXCallback(Callback):
    _order=2
    def __init__(self,tfm): self.tfm=tfm
    def begin_batch(self):self.run.xb = self.tfm(self.xb)

def view_tfm(*size):
    def _inner(x): return x.view(*((-1,)+size))
    return _inner

def children(m): return list(m.children())

class Hook():
    def __init__(self,m,f):
        # model is the layer and f is the callback function
        self.hook = m.register_forward_hook(partial(f,self))
    def remove(self): self.hook.remove()
    def __del__(self): self.remove()

def append_stats(hook,module,inp,outp):
    if not hasattr(hook,'stats'):hook.stats = ([],[])
    means,stds = hook.stats
    means.append(outp.data.mean())
    stds.append(outp.data.std())

class ListContainer():
    def __init__(self,items):self.items=listify(items)
    def __getitem__(self,idx):
        if isinstance(idx,(int,slice)):return self.items[idx]
        if isinstance(idx[0],bool):
            assert(len(idx)==len(self))# boolean masking
            return [o for m,o in zip(idx,self.items) if m]
        return [self.items[i] for i in idx]
    def __len__(self):return len(self.items)
    def __iter__(self):return iter(self.items)
    def __setitem__(self,i,o): self.items[i] = o
    def __delitem__(self,i): del(self,items[i])
    def __repr__(self):
        res = f'{self.__class__.__name__} ({len(self)}items)\n{self.items[:10]}'
        if len(self)>10:res = res[:-1] +'...]'
        return res

from torch.nn import init

class Hooks(ListContainer):
    def __init__(self,ms,f):super().__init__([Hook(m,f) for m in ms])
    def __enter__(self,*args): return self
    def __exit__(self,*args): self.remove()
    # dunder enter and exit allow the usage of "with"
    def __del__(self): self.remove()

    def __delitem(self,i):
        self[i].remove()
        # deleting then dereferencing
        super().__delitem__(i)

    def remove(self):
        for h in self: h.remove()


def get_cnn_layers(data, nfs, layer, **kwargs):
    nfs = [1] + nfs
    return [layer(nfs[i], nfs[i+1], 5 if i==0 else 3, **kwargs)
            for i in range(len(nfs)-1)] + [
        nn.AdaptiveAvgPool2d(1), Lambda(flatten), nn.Linear(nfs[-1], data.c)]
    # i for Conv and i+1 for ReLU

def conv_layer(ni, nf, ks=3, stride=2, **kwargs):
    return nn.Sequential(
        nn.Conv2d(ni, nf, ks, padding=ks//2, stride=stride), GeneralRelu(**kwargs))


class GeneralRelu(nn.Module):
    def __init__(self,leak=None,sub=None,maxv=None):
        super().__init__()
        self.leak,self.sub,self.maxv = leak,sub,maxv

    def forward(self,x):
        x = F.leaky_relu(x,self.leak) if self.leak is not None else F.relu(x)
        if self.sub is not None: x.sub_(self.sub)
        if self.maxv is not None: x.clamp_max_(self.maxv)
        return x

def init_cnn(m,uniform=False):
    # look into opportunity costs for uniform initialisation
    # instead of normal (Gaussian) initialisation
    f = init.kaiming_uniform_ if uniform else init.kaiming_normal_
    for l in m:
        if isinstance(l,nn.Sequential):
            f(l[0].weight,a=0.1)
            l[0].bias.data.zero_()

def get_cnn_model(data,nfs,layer,**kwargs):
    return nn.Sequential(*get_cnn_layers(data,nfs,layer,**kwargs))


def get_learn_run(nfs,data,lr,layer,cbs=None,opt_func=None,uniform=False,**kwargs):
    model = get_cnn_model(data,nfs,layer,**kwargs)
    init_cnn(model,uniform=uniform)
    return get_runner(model,data,lr=lr,cbs=cbs,opt_func=opt_func)
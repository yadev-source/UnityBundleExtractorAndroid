def __getattr__(n): return type('Dummy', (), {'__call__': lambda *a, **k: None, '__getattr__': lambda s,n: __getattr__(n)})()

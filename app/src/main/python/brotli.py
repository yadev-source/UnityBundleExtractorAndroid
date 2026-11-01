# Dummy brotli - most bundles don't use brotli compression
def decompress(data):
    raise RuntimeError("This bundle uses brotli compression - not supported on this Android build, use PC version")
def compress(data):
    raise RuntimeError("brotli not available")
def error():
    pass
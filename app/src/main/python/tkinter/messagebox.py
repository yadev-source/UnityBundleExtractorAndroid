# Dummy messagebox with all constants tkinter expects
YES = "yes"
NO = "no"
OK = "ok"
CANCEL = "cancel"
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
ABORTRETRYIGNORE = "abortretryignore"

def showinfo(*a, **k): return OK
def showerror(*a, **k): return OK
def showwarning(*a, **k): return OK
def askyesno(*a, **k): return False
def askyesnocancel(*a, **k): return None
def askokcancel(*a, **k): return False
def askretrycancel(*a, **k): return False
def askquestion(*a, **k): return NO

# Biar from tkinter.messagebox import apa aja gak error
def __getattr__(name):
    return 0

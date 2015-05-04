

'''
2) 条件表达式的编写应该足够 pythonic，如以下形式的条件表达式是拙劣的：
if len(alist) != 0: do_something()
if alist != []: do_something()
if s != “”: do_something()
if var != None: do_something()
if var != False: do_something()
上面的语句应该写成：
if seq: do_somethin() # 注意，这里命名也更改了
if var: do_something()
'''
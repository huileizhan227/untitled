def join_url(*args):
    if len(args) <= 1:
        raise ValueError('at least two args')
    new_url = ''
    args = list(args)
    for i in range(len(args) - 1):
        if not args[i].endswith('/'):
            args[i] += '/'
    for i in range(1, len(args)):
        if args[i].startswith('/'):
            args[i] = args[i][1:]
    return ''.join(args)

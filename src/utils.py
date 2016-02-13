def parse_pkgname(pkgname):
    package, version = None, None
    try:
        idx = pkgname.rindex('@')
        package, version = pkgname[:idx], pkgname[idx+1:]
    except ValueError as exc:
        package, version = pkgname, '*'
    return package, version

def get_octal_from_file_permission(rwx: str) -> str:
    u, g, o = rwx[:3], rwx[3:6], rwx[6:]

    def rwx_to_o(a: str) -> str:
        ao = (4 if 'r' in a else 0) + (2 if 'w' in a else 0) + (1 if 'x' in a else 0)
        return str(ao)

    return rwx_to_o(u) + rwx_to_o(g) + rwx_to_o(o)

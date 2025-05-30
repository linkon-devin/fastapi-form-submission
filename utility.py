
def get_tt_number_from_type(tt):
    return tt[3:] if tt.startswith("tt_") else None

def get_tt_number_from_line(tt_line):
    parts = tt_line.split(maxsplit=1)
    if parts: # Ensure there's at least one part
        return parts[0]
    return None

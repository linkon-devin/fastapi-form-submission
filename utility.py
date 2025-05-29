
def get_tt_number(tt):
    return tt[3:] if tt.startswith("tt_") else None
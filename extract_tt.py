def extract_tt_data(receipt_data_string):
    tt_lines = []
    lines = receipt_data_string.strip().split('\n')

    # The TT data consistently starts at index 29 (the 30th character)
    TT_START_INDEX = 29

    for line in lines:
        # 1. Skip empty lines or lines that become empty after stripping
        if not line.strip():
            continue

        # 2. Skip known header lines like "SESSION="
        if line.startswith("SESSION="):
            continue

        # 3. Ensure the line is long enough to contain data at the expected TT start position
        if len(line) > TT_START_INDEX:
            # Extract the segment that should contain the TT data
            extracted_segment = line[TT_START_INDEX:].strip()

            # 4. Perform the new filtering: Check if the first value is '0' or '00'
            if extracted_segment: # Ensure the segment isn't empty after stripping
                # Split the segment to get the very first space-separated value
                # maxsplit=1 is efficient as we only need the first part
                first_value_str = extracted_segment.split(maxsplit=1)[0]

                # Check if this first value is exactly '0' or '00'
                if first_value_str == '0' or first_value_str == '00':
                    continue # Skip this line, as its TT identifier is invalid

                # If it passes all checks, add it to our list
                tt_lines.append(extracted_segment)

    return tt_lines

receipt_data = """
SESSION=1157
6666 150   3   1 06002 00000  01 0 0 0 0 845  0000008880171    1.000      1.00
   00000000 0 sess: 1157     13 0 0 0 0 16  0000000000050    0.000      0.00
   30.05.25 12:30:45          61 0 1 Fejl 0000000000055    
   rec: 2  0/0                 23 0 0 000 1 0.00 -100.00   0.00   101.00
6666 150   3   2 06002 00000  47 0 0 004 0 0.00   0.00   1.00     1.00
   00000000 0 sess: 1157     64 0 0 001 0 0.00   1.00  25.00     1.00
   30.05.25 12:30:45          21 0 0 0  0 0 0     0.80     1.00
   rec: 3  0/0                 22 0 1 23  5 0 1     0.00     1.00
6666 150   3   3 06002 00000  09 0 0 0 0 0  0000000000063    0.000      0.00
   00000000 0 sess: 1157     00 
   30.05.25 12:30:45          00  
   rec: 4  0/0                 00 
"""

expected_tts = [
    "01 0 0 0 0 845  0000008880171    1.000      1.00",
    "13 0 0 0 0 16  0000000000050    0.000      0.00",
    "61 0 1 Fejl 0000000000055",
    "23 0 0 000 1 0.00 -100.00   0.00   101.00",
    "47 0 0 004 0 0.00   0.00   1.00     1.00",
    "64 0 0 001 0 0.00   1.00  25.00     1.00",
    "21 0 0 0  0 0 0     0.80     1.00",
    "22 0 1 23  5 0 1     0.00     1.00",
    "09 0 0 0 0 0  0000000000063    0.000      0.00"
]

extracted_tts = extract_tt_data(receipt_data)

try:
    assert(expected_tts == extracted_tts)
except AssertionError:
    print("tt extraction error ")
from utility import get_tt_number_from_type, get_tt_number_from_line
from extract_tt import extract_tt_data
from typing import List

def decode_ut(bits_description, ut_val):
    decoded = []
    for i, (off, on) in enumerate(bits_description):
        if ut_val & (1 << i):
            decoded.append(f"  - Bit {i}: {on}")
    return decoded

def find_tt_lines_by_type(tt_lines_list:List[str], target_tt_number) -> List[str]:
    ttlines = []
    print("tt_number", target_tt_number)
    if target_tt_number is None:
        print(f"Error: Invalid TT type parameter format: '{target_tt_number}'. Expected 'tt_XX'.")
        return None

    for tt_line in tt_lines_list:
        line_tt_number = get_tt_number_from_line(tt_line)
        if line_tt_number == target_tt_number:
            ttlines.append(tt_line)

    return ttlines

def find_tt_line_by_type(tt_lines_list:List[str], target_tt_number) -> List[str]:
    print("tt_number", target_tt_number)
    if target_tt_number is None:
        print(f"Error: Invalid TT type parameter format: '{target_tt_number}'. Expected 'tt_XX'.")
        return None

    for tt_line in tt_lines_list:
        line_tt_number = get_tt_number_from_line(tt_line)
        if line_tt_number == target_tt_number:
            return tt_line

    return None

def decode_tt(receipt: str, ttOption: str = "tt_01"):
    extracted_tts = extract_tt_data(receipt)
    target_tt_number = get_tt_number_from_type(ttOption)
    tt_lines = find_tt_lines_by_type(extracted_tts, target_tt_number)
    print("multilines: ", decode_transaction_list(tt_lines, target_tt_number))
    tt_line = find_tt_line_by_type(extracted_tts, target_tt_number)
    return decode_transaction_list(tt_lines, target_tt_number)

def decode_transaction_list(tt_lines: List[str], target_tt_number) -> List[str]:
    return [decode_transaction(x, target_tt_number) for x in tt_lines]

def decode_transaction(tt_line: str, target_tt_number) -> str:
    values = tt_line.strip().split()
    if not values or len(values) < 2:
        return "Invalid input."
    
    print(f"Decoding transaction with value: {values}")
    tt_type = target_tt_number
    print("tt type", tt_type)

    if tt_type == "01":
        return decode_tt01(values)
    elif tt_type == "06":
        return decode_tt06(values)
    elif tt_type == "19":
        return decode_tt19(values)
    elif tt_type == "24":
        return decode_tt24(values)
    elif tt_type == "47":
        return decode_tt47(values)
    elif tt_type == "61":
        return decode_tt61(values)
    elif tt_type == "07":
        return decode_tt07(values)
    elif tt_type == "13":
        return decode_tt13(values)
    elif tt_type == "02":
        return decode_tt02(values)
    elif tt_type == "08":
       return decode_tt08(values)
    elif tt_type == "10":
       return decode_tt10(values)
    elif tt_type == "14":
       return decode_tt14(values)
    elif tt_type == "18":
       return decode_tt18(values)
    elif tt_type == "20":
       return decode_tt20(values)
    elif tt_type == "22":
       return decode_tt22(values)
    elif tt_type == "23":
       return decode_tt23(values)
    elif tt_type == "26":
       return decode_tt26(values)
    elif tt_type == "32":
       return decode_tt32(values)
    elif tt_type == "34":
      return decode_tt34(values)
    
    else:
        return f"Unsupported TT type: {tt_type}"

def decode_tt01(values):
    ut_bit_meanings = [
        ("Article No keyed in", "Article scanned"),
        ("Sales", "Articles returned"),
        ("Normal", "Enquiry"),
        ("Automatic", "Manual (price)"),
        ("Normal", "<KPRI>"),
        ("Normal", "Selfscanned"),
        ("Normal", "<VOID/TBF>"),
        ("Normal", "<CANCEL>")
    ]

    keys = ["ut", "L0", "antpk", "retspc", "L1", "varenr", "antal", "bel"]
    data = dict(zip(keys, values[1:]))

    output = ["Transaction Type: tt01 - Article Sale", "\nField Breakdown:"]
    ut_val = int(data["ut"])
    output.append(f"• ut = {ut_val} (Binary: {ut_val:08b})")
    output.extend(decode_ut(ut_bit_meanings, ut_val))

    output.append(f"• L0 = {data['L0']} (Handling time in seconds)")
    output.append(f"• antpk = {data['antpk']} (Number of packets (weight-variable articles))")
    output.append(f"• retspc = {data['retspc']} (Specification on returned article)")
    output.append(f"• L1 = {data['L1']} (Article group or classification)")
    output.append(f"• varenr = {data['varenr']} (Article number)")
    output.append(f"• antal = {data['antal']} (Quantity)")
    output.append(f"• bel = {data['bel']} (Line amount)")
    return "\n".join(output)


def decode_tt06(values):
    ut_bit_meanings = [
        ("Article No keyed in", "Article scanned"),
        ("Sales", "Articles returned"),
        ("$ discount", "Percent discount"),
        ("Automatic", "Manual"),
        ("Normal discount", "Club discount"),
        ("Normal", "Selfscanned")
    ]

    discount_types = {
        0: "Article decided",
        1: "Tender type decided",
        2: "Till decided",
        3: "Receipt total decided",
        5: "Basket discount",
        6: "Coupon discount",
        7: "Price guarantee discount",
        8: "Markdown discount",
        9: "Customer/article discount",
        10: "External discount",
        11: "Club discount",
        12: "Free item discount",
        13: "Point discount",
        14: "Total discount (<TOTD>-precoding)",
        15: "Customer list discount",
        16: "Best price discount",
        17: "Manual group discount (=smart discount)"
    }

    keys = ["ut", "L0", "antpk", "retspc", "L1", "varenr", "antal", "bel"]
    data = dict(zip(keys, values[1:]))

    output = ["Transaction Type: tt06 - Article Discount", "\nField Breakdown:"]
    ut_val = int(data["ut"])
    output.append(f"• ut = {ut_val} (Binary: {ut_val:06b})")
    output.extend(decode_ut(ut_bit_meanings, ut_val))

    l0_val = int(data["L0"])
    output.append(f"• L0 = {l0_val} (Discount type: {discount_types.get(l0_val, 'Unknown')})")
    output.append(f"• antpk = {data['antpk']} (Coupon ID (only if L0=6))")
    output.append(f"• retspc = {data['retspc']} (Return reason code)")
    output.append(f"• L1 = {data['L1']} (Article group or classification)")
    output.append(f"• varenr = {data['varenr']} (Article number)")
    output.append(f"• antal = {data['antal']} (Percent rate)")
    output.append(f"• bel = {data['bel']} (Line amount)")
    return "\n".join(output)

def decode_tt19(values):
    discount_types = {
        0: "Not used",
        1: "Automatically discount as net amount",
        2: "Automatically discount as gross amount",
        3: "Manual discount or article group discount",
        4: "Receipt or tender defined discount",
        5: "Basket discount",
        6: "Back distributed coupon discount",
        7: "Price guaranty discount",
        8: "Markdown discount",
        9: "Customer/article discount",
        10: "External discount",
        11: "Club discount",
        12: "Free item discount",
        13: "Point discount",
        14: "Totaldiscount (<TOTD>-precoding)",
        15: "Customer list discount",
        16: "Best price discount",
        17: "Manual group discount (=smart discount)"
    }

    keys = ["ut", "L0", "antpk", "retspc", "L1", "varenr", "antal", "bel"]
    data = dict(zip(keys, values[1:]))

    l1 = int(data["L1"])
    output = [f"Transaction Type: tt19 - Printed Discount (format A)",
              f"\n• L1 = {l1} ({discount_types.get(l1, 'Unknown')})"]

    ut_val = int(data["ut"])
    output.append(f"• ut = {ut_val} (Binary: {ut_val:08b})")

    if l1 in (1, 2):
        output.append("Automatically discount lines:")
        output.append(f"• L0 = {data['L0']} (Discount text)")
        output.append(f"• varenr = {data['varenr']} (Article number)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 == 3:
        bit2 = bool(ut_val & (1 << 2))
        bit3 = bool(ut_val & (1 << 3))
        output.append("Manual discount or article group discount:")
        output.append(f"• Discount Type = {'Percent' if bit2 else 'Amount'}")
        output.append(f"• Mode = {'Manual' if bit3 else 'Automatic'}")
        output.append(f"• Discount Reason Code = {data['retspc'] if bit3 else 'N/A'}")
        output.append(f"• varenr = {data['varenr']} (Article number)")
        output.append(f"• antal = {data['antal']} (Optional percent value)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 == 4:
        output.append("Receipt or tender defined discount:")
        output.append(f"• varenr = {data['varenr']} (Service code)")
        output.append(f"• antal = {data['antal']} (Optional percent)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 == 5:
        output.append("Basket discount:")
        output.append(f"• L0 = {data['L0']} (Text segment)")
        output.append(f"• varenr = {data['varenr']} (Basket number)")
        output.append(f"• antal = {data['antal']} (Total basket price)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 == 6:
        output.append("Distributed coupon discount:")
        output.append(f"• L0 = {data['L0']} (Text segment)")
        output.append(f"• varenr = {data['varenr']} (Coupon ID)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 == 7:
        output.append("Price guaranty discount:")
        output.append(f"• varenr = {data['varenr']} (Company ID)")
        output.append(f"• antal = {data['antal']} (Total price from competitor)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    elif l1 in (8, 9):
        bit0 = bool(ut_val & (1 << 0))
        bit2 = bool(ut_val & (1 << 2))
        bit3 = bool(ut_val & (1 << 3))
        output.append(f"{discount_types[l1]}:")
        output.append(f"• Entry = {'Scanned' if bit0 else 'Keyed'}")
        output.append(f"• Discount Type = {'Percent' if bit2 else 'Amount'}")
        output.append(f"• Mode = {'Manual' if bit3 else 'Automatic'}")
        output.append(f"• varenr = {data['varenr']} (Article number)")
        output.append(f"• antal = {data['antal']} (Percent value)")
        output.append(f"• bel = {data['bel']} (Discount amount)")
    else:
        output.append("Default parsing (structure unknown for this L1):")
        for k, v in data.items():
            output.append(f"• {k} = {v}")

    return "\n".join(output)

def decode_tt24(values):
    card_types = {
        0: "Card number contains an account number",
        1: "Card number contains a card number",
        2: "Card number contains a PCI-truncated card number"
    }

    transaction_types = {
        6: "Void",
        7: "Cancel"
    }

    keys = ["ut", "L0", "L01", "L02", "afr", "L1", "oknok", "flag", "cardnr", "bel"]
    data = dict(zip(keys, values[1:]))

    ut_val = int(data["ut"])
    output = [f"Transaction Type: tt24 - Paid with Creditcards (format D)"]

    output.append(f"• ut = {ut_val} (Binary: {ut_val:08b})")

    # Handle specific flags
    flag_value = int(data["flag"])
    output.append(f"• flag = {flag_value} ({card_types.get(flag_value, 'Unknown')})")

    # Handle special transactions
    if ut_val & (1 << 6):
        output.append("• Transaction type: Void")
    elif ut_val & (1 << 7):
        output.append("• Transaction type: Cancel")

    # Card issuer and sequence numbers
    output.append(f"• Card Issuer ID: {data['L0']} (Card serial number / Reservation ID)")
    output.append(f"• Card Issuer ID (L01): {data['L01']}")
    output.append(f"• Card Sequence Number (L02): {data['L02']}")

    # Rounding info
    output.append(f"• Rounding up decimals (afr): {data['afr']}")

    # Tender code and Grouping number
    output.append(f"• Tender code (L1): {data['L1']}")
    output.append(f"• Grouping number (oknok): {data['oknok']}")

    # Card number and payment amount
    output.append(f"• Card/Account number (cardnr): {data['cardnr']}")
    output.append(f"• Amount paid (bel): {data['bel']}")

    return "\n".join(output)

def decode_tt47(values):
    transaction_types = {
        0: "Staff",
        1: "Customer",
        2: "Club",
        3: "Bonus Program",
        4: "External Customer",
        5: "Cardholder ID",
        6: "Bonus Point Balance",
        7: "Project Number"
    }

    keys = ["ut", "L0", "afr", "L1", "oknok", "L5", "L2", "bel"]
    data = dict(zip(keys, values[1:]))

    ut_val = int(data["ut"])
    oknok_val = data["oknok"]
    output = [f"Transaction Type: tt47 - Additional Sales Info (format C)"]

    # Decode the ut (binary values)
    output.append(f"• ut = {ut_val} (Binary: {ut_val:08b})")
    if ut_val & (1 << 0):
        output.append("  - Extended Discount System (formed via the extended discount system)")
    if ut_val & (1 << 1):
        output.append("  - Contains points (pointtype 1-9)")

    # oknok (Subtype)
    output.append(f"• oknok = {oknok_val} - {transaction_types.get(oknok_val, 'Unknown subtype')}")

    # Handling based on oknok values
    if oknok_val == 0:
        output.append("  - Staff: Sale accumulated in f153.")
    elif oknok_val == 1:
        output.append("  - Customer: Sale accumulated in f153, bonus calculated from turnover.")
    elif oknok_val == 2:
        output.append("  - Club: Discount redeemed instantly.")
    elif oknok_val == 3:
        output.append("  - Bonus Program: Created per receipt. More bonus cards can be linked.")
    elif oknok_val == 4:
        output.append("  - External Customer: Afr contains the first 4 digits.")
    elif oknok_val == 5:
        output.append("  - Cardholder ID: Card sequence number replaced when ID > 2 digits.")
    elif oknok_val == 6:
        output.append("  - Bonus Point Balance: Points balance from external system.")
    elif oknok_val == 7:
        output.append("  - Project Number: In L5 field.")

    # Details of the record
    output.append(f"• L0 (oknok = {oknok_val}): {data['L0']}")
    output.append(f"• Card sequence number (afr): {data['afr']}")
    output.append(f"• Discount Group (L1): {data['L1']}")
    output.append(f"• Staff/Customer/Member Number (L5): {data['L5']}")
    output.append(f"• Sale Entitled to Discount (L2): {data['L2']}")
    output.append(f"• Total Amount on Receipt (bel): {data['bel']}")

    return "\n".join(output)

def decode_tt61(values):
    """
    Decode TT61 input and parse the data based on the structure:
    Example input: '61 8 53 dsgd'
    
    :param values: List of values parsed from the input string
    :return: Decoded transaction string
    """
    if len(values) < 4:
        return "Invalid TT61 input, insufficient values."

    tt_type = values[0]  # Expected "61"
    ut = int(values[1])   # The 'ut' value (bit flags)
    L0 = int(values[2])   # The 'L0' value (transaction code)
    tekst = " ".join(values[3:])  # The remaining part is the remark text

    # Decode 'ut' flags
    ut_flags = {
        'was_scanned': bool(ut & (1 << 0)),     # bit 0
        'is_returned': bool(ut & (1 << 1)),     # bit 1
        'meaning_2': bool(ut & (1 << 2)),       # bit 2
        'self_scanned': bool(ut & (1 << 5)),    # bit 5
    }

    # Descriptions for different L0 values
    l0_descriptions = {
        1: "Article not found",
        2: "EFT printlines",
        4: "Reference ID at selfscanning",
        5: "Reference ID at kontrolscanning",
        6: "Scanning error",
        9: "Logmessage concerning creditcards",
        12: "REA Gift Voucher",
        14: "Generic error message",
        15: "Random control",
        16: "Discount coupon registered",
        20: "Header for hashed values",
        21: "Credit card hash part 1",
        22: "Credit card hash part 2",
        23: "Credit card hash part 3",
        28: "External customer ID",
        31: "POS Program file and version",
        32: "Restaurant table",
        33: "Restaurant chair",
        37: "Loyalty ID part 1",
        38: "Loyalty ID part 2",
        39: "EFT serial number",
        47: "External giftcard number",
        50: "GQ/General Query",
        51: "Signature",
        53: "Free discount text",
        62: "Message from tinting machine",
        101: "Customer Name",
        102: "Customer Address",
        103: "Zipcode and City",
        104: "Phone Number",
        105: "Email",
        106: "Remarks",
        107: "VAT Number",
        108: "Customer Reference",
        109: "Requisition ID",
        110: "Customer Label",
        111: "Customer Label Rec ID"
    }

    description = l0_descriptions.get(L0, "Unknown or custom L0 value")

    # Build the result string
    result = (
        f"TT Type: {tt_type}\n"
        f"UT Flags: {ut_flags}\n"
        f"L0: {L0} - {description}\n"
        f"Remark Text: {tekst}"
    )

    return result

def decode_tt07(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT07 input. Expected at least 8 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)  # Join any remaining parts (discount amount)

    ut_int = int(ut)
    ut_flags = []
    if ut_int & 1:
        ut_flags.append("New system")
    else:
        ut_flags.append("Old system")
    if ut_int & 2:
        ut_flags.append("Service transaction")
    if ut_int & 4:
        ut_flags.append("Tender transaction")
    if not (ut_int & 2) and not (ut_int & 4):
        ut_flags.append("No bookkeeping")

    antpk_info = "Service code/tender type present" if int(antpk) & 1 else "Standard"

    return (
        f"TT07 - Undistributed Discount:\n"
        f"  System type      : {', '.join(ut_flags)}\n"
        f"  Line number      : {l0}\n"
        f"  ANT-PK Flag      : {antpk_info}\n"
        f"  Discount group   : {retspc}\n"
        f"  Article group    : {l1}\n"
        f"  Article number   : {varenr}\n"
        f"  Discount rate    : {antal}\n"
        f"  Discount amount  : {bel}"
    )

def decode_tt13(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT13 input. Expected at least 8 fields."

    _, ut, l0, xx, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)

    l1_type = int(l1)
    ut_int = int(ut)
    ut_bits = lambda n: bool(ut_int & (1 << n))

    description = f"TT13 - Additional Article Info:\n"
    description += f"  UT Flags         : {ut} (raw)\n"
    description += f"  Line number      : {l0}\n"
    description += f"  XX field         : {xx}\n"
    description += f"  Discount group   : {retspc}\n"
    description += f"  L1 Type          : {l1} - "

    if l1_type == 1:
        description += "Delivery number (prompt)\n"
    elif l1_type == 2:
        description += "Delivery number (manual)\n"
    elif l1_type == 3:
        description += "Day-of-arrival (DOA)\n"
    elif l1_type == 11:
        description += "Concessions transaction\n"
    elif l1_type == 12:
        rule = antal
        allowed = "Yes" if bel == "1" else "No"
        description += "Rules for article sales\n"
        description += f"  Rule number      : {rule}\n"
        description += f"  Allowed          : {allowed}\n"
    elif l1_type == 13:
        description += "Vensafe\n"
        description += f"  Product ID       : {varenr}\n"
        description += f"  Serial no.       : {bel}\n"
    elif l1_type == 14:
        description += "Additional article (e.g. bottles)\n"
        description += f"  Main Article No. : {varenr}\n"
        description += f"  Article suffix   : {bel}\n"
    elif l1_type == 15:
        description += "Markdown reference\n"
        description += f"  Article No.      : {varenr}\n"
        description += f"  Reference No.    : {bel}\n"
        description += f"  Original Price   : {antal}\n"
    elif l1_type == 16:
        description += "Referred article\n"
        description += f"  Original Article : {varenr}\n"
    elif l1_type == 17:
        description += "Bottle refund as article\n"
        description += f"  Article No.      : {varenr}\n"
        description += f"  Refund ID        : {bel}\n"
        description += f"  Refund Amount    : {antal}\n"
        description += f"  Flags            : "
        flags = []
        if ut_bits(0): flags.append("Scanned")
        if ut_bits(1): flags.append("Offline mode")
        if ut_bits(2): flags.append("Amount from server")
        if ut_bits(6): flags.append("VOID")
        if ut_bits(7): flags.append("CANCEL")
        description += ", ".join(flags) if flags else "None"
        description += "\n"
    elif l1_type == 18:
        description += "Connected retail\n"
        description += f"  Article No.      : {varenr}\n"
    elif l1_type == 19:
        description += "Reply for variant/modifier question\n"
        is_modifier = ut_bits(0)
        description += f"  Article No.      : {varenr}\n"
        description += f"  Variant/Mod ID   : {antal}\n"
        description += f"  Answer           : {bel}\n"
        description += f"  Type             : {'Modifier' if is_modifier else 'Variant'}\n"
    else:
        description += "Unknown L1 type\n"
        description += f"  Article No.      : {varenr}\n"
        description += f"  Quantity         : {antal}\n"
        description += f"  Extra Info       : {bel}\n"

    return description.strip()

def decode_tt02(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT02 input. Expected at least 9 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)

    ut_int = int(ut)
    ut_bits = lambda n: bool(ut_int & (1 << n))

    flags = []
    if ut_bits(0): flags.append("Article Sale")
    if ut_bits(1): flags.append("Service Charge")
    if ut_bits(2): flags.append("Discount")

    vat_percent = int(antpk) / 100

    description = f"TT02 - Line VAT Info:\n"
    description += f"  UT Flags         : {ut} ({', '.join(flags) if flags else 'None'})\n"
    description += f"  Line Number      : {l0}\n"
    description += f"  VAT Percentage   : {vat_percent:.2f}%\n"
    description += f"  VAT Code         : {retspc}\n"
    description += f"  L1               : {l1}\n"
    description += f"  Article/Service  : {varenr}\n"
    description += f"  VAT Amount       : {antal}\n"
    description += f"  Amount excl. VAT : {bel}\n"

    return description.strip()

def decode_tt08(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT08 input. Expected at least 9 fields."

    _, ut, l0, xx, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)

    ut_int = int(ut)
    ut_bits = lambda n: bool(ut_int & (1 << n))

    flags = []
    if ut_bits(0): flags.append("Scanned (SNI=0)")
    else: flags.append("Article not keyed in")

    if ut_bits(1): flags.append("Article Returned (SNI=0)")
    else: flags.append("Sales")

    if ut_bits(5): flags.append("Self-scanned")
    else: flags.append("Normal (not self-scanned)")

    description = f"TT08 - VAT Correction:\n"
    description += f"  UT Flags               : {ut} ({', '.join(flags)})\n"
    description += f"  Line Number            : {l0}\n"
    description += f"  XX                     : {xx}\n"
    description += f"  Return Specification   : {retspc}\n"
    description += f"  Article Group (L1)     : {l1}\n"
    description += f"  Article Number         : {varenr}\n"
    description += f"  Quantity (Antal)       : {antal}\n"
    description += f"  Amount                 : {bel}\n"

    return description.strip()

def decode_tt10(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT10 input. Expected at least 8 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)

    description = f"TT10 - Exchange Stickers:\n"
    description += f"  UT Flags               : {ut}\n"
    description += f"  Original Store No (L0) : {l0}\n"
    description += f"  Receipt No (antpk)     : {antpk}\n"
    description += f"  Retspc                 : {retspc}\n"
    description += f"  Terminal No (L1)       : {l1}\n"
    description += f"  Sticker ID (varenr)    : {varenr}\n"
    description += f"  Quantity (antal)       : {antal}\n"
    description += f"  Operation Date (bel)   : {bel} (YYMMDD)\n"

    return description.strip()

def decode_tt14(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT14 input. Expected at least 8 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel)

    # Bit interpretations for UT
    ut_flags = int(ut, 16) if ut.startswith(("0x", "0X")) else int(ut)

    flag_desc = []
    if ut_flags & (1 << 0): flag_desc.append("Scanned")
    if ut_flags & (1 << 1): flag_desc.append("Redeemed")
    if ut_flags & (1 << 2): flag_desc.append("Unique Coupon")
    if ut_flags & (1 << 3): flag_desc.append("Finance Transaction")
    if ut_flags & (1 << 4): flag_desc.append("Tender Type")

    flag_summary = ", ".join(flag_desc) if flag_desc else "None"

    description = f"TT14 - Discount Coupons:\n"
    description += f"  UT Flags                : {ut} ({flag_summary})\n"
    description += f"  Security Code (L0)      : {l0}\n"
    description += f"  Service/Tender Type     : {antpk}\n"
    description += f"  Retspc                  : {retspc}\n"
    description += f"  Coupon ID (L1)          : {l1}\n"
    description += f"  Store + Coupon No       : {varenr}\n"
    description += f"  Quantity (antal)        : {antal}\n"
    description += f"  Value (bel)             : {bel} (Issued/Redeemed)\n"

    return description.strip()

def decode_tt18(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT18 input. Expected at least 8 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    # Interpret L0
    l0_map = {
        "0": "Undefined",
        "1": "Family Number",
        "2": "Discount Group Number"
    }
    l0_desc = l0_map.get(l0, "Unknown")

    # Interpret retspc
    retspc_map = {
        "0": "Undefined",
        "1": "Campaign Number",
        "2": "Offer ID"
    }
    retspc_desc = retspc_map.get(retspc, "Unknown")

    description = f"TT18 - Datacarrier:\n"
    description += f"  UT                      : {ut}\n"
    description += f"  L0                      : {l0} ({l0_desc})\n"
    description += f"  Antpk                   : {antpk}\n"
    description += f"  Retspc                  : {retspc} ({retspc_desc})\n"
    description += f"  L1                      : {l1}\n"
    description += f"  Varenr                  : {varenr}\n"
    description += f"  Antal                   : {antal}\n"
    description += f"  Bel                     : {bel}\n"

    return description.strip()

def decode_tt20(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT20 input. Expected at least 9 fields."

    _, ut, l0, antpk, retspc, l1, varenr, antal, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    # Decode bit flags in UT
    ut_flags = []
    ut_bin = int(ut, 16) if ut.startswith("0x") else int(ut)
    if ut_bin & (1 << 0): ut_flags.append("Scanned")
    else: ut_flags.append("Article keyed in")
    if ut_bin & (1 << 1): ut_flags.append("Articles returned")
    else: ut_flags.append("Sales")
    if ut_bin & (1 << 2): ut_flags.append("Inquiry")
    else: ut_flags.append("Normal")
    if ut_bin & (1 << 3): ut_flags.append("Manual price")
    else: ut_flags.append("Automatic")
    if ut_bin & (1 << 6): ut_flags.append("VOID")
    if ut_bin & (1 << 7): ut_flags.append("CANCEL")

    # Interpret L1 (service type)
    l1_map = {
        "0": "Normal service transaction",
        "1": "Fee related to tender type",
        "2": "Fee related to FORS & EXCL",
        "3": "Staff discount",
        "4": "Coupon redemption",
        "5": "Receipt discount"
    }
    l1_desc = l1_map.get(l1, "Unknown")

    description = f"TT20 - Services:\n"
    description += f"  UT                      : {ut} ({', '.join(ut_flags)})\n"
    description += f"  L0 (Handling Time)      : {l0}\n"
    description += f"  Antpk (% Rate)          : {antpk}\n"
    description += f"  Retspc (Return Reason)  : {retspc}\n"
    description += f"  L1 (Service Type)       : {l1} ({l1_desc})\n"
    description += f"  Varenr (Service No.)    : {varenr}\n"
    description += f"  Antal (Quantity)        : {antal}\n"
    description += f"  Bel (Line Amount)       : {bel}\n"

    return description.strip()


def decode_tt22(values: list[str]) -> str:
    if len(values) < 8:
        return "Invalid TT22 input. Expected at least 8 fields."

    _, ut, l0, xxx, l1, bettid, annlin, antlin, annbel, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    description = f"TT22 - Total (format B):\n"
    description += f"  UT                          : {ut}\n"
    description += f"  L0 (No. of articles)        : {l0} (rules: dec.code = 1, triggered articles ignored, returns/rollbacks counted negative)\n"
    description += f"  XXX                         : {xxx}\n"
    description += f"  L1 (Attendance Time)        : {l1} sec\n"
    description += f"  Bettid (Payment Time)       : {bettid} sec\n"
    description += f"  Annlin (Deleted Lines)      : {annlin}\n"
    description += f"  Antlin (Total Article Lines): {antlin}\n"
    description += f"  Annbel (Deleted Amount)     : {annbel}\n"
    description += f"  Bel (Receipt Total)         : {bel}\n"

    return description.strip()

def decode_tt23(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT23 input. Expected at least 9 fields."

    _, ut, l0, afr, l1, oknok, l5, l2, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    description = f"TT23 - Payments (non-card/currency) (format C):\n"
    description += f"  UT                          : {ut} (bit 1: CMS, bit 6: VOID, bit 7: CANCEL)\n"
    description += f"  L0                          : {l0}\n"
    description += f"  AFR (Decimal Rounding)     : {afr}\n"
    description += f"  L1 (Tender Code)            : {l1}\n"
    description += f"  OKNOK (Grouping Number)     : {oknok}\n"
    description += f"  L5 (Change)                 : {l5}\n"
    description += f"  L2 (Bank Reg No. etc.)      : {l2}\n"
    description += f"  BEL (Amount Paid)           : {bel}\n"

    return description.strip()

def decode_tt26(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT26 input. Expected at least 9 fields."

    _, ut, l0, afr, l1, oknok, l5, l2, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    description = f"TT26 - Redeemed Bonus Points (format C):\n"
    description += f"  UT (Point type bits 0-3)     : {ut} (bit 6: TILB, bit 7: SLET)\n"
    description += f"  L0 (Reservation ID)          : {l0}\n"
    description += f"  AFR (Rounding)               : {afr}\n"
    description += f"  L1 (Tender Code)             : {l1} {'(Stampcard for discounts)' if l1.startswith('-') else ''}\n"
    description += f"  OKNOK (Grouping Number)      : {oknok}\n"
    description += f"  L5 (Member Number)           : {l5}\n"
    description += f"  L2 (Points)                  : {l2}\n"
    description += f"  BEL (Point Value)            : {bel}\n"

    return description.strip()

def decode_tt32(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT32 input. Expected at least 9 fields."

    _, ut_str, l0, afr, l1, oknok, l5, l2, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    ut = int(ut_str)
    is_refund = bool(ut & (1 << 1))  # bit 1

    ut_description = []
    ut_description.append(f"bit 1 (Refund)           : {'ON (refund)' if is_refund else 'OFF (sale)'}")

    description = f"TT32 - Additional data at order/receipt level (format C):\n"
    description += f"  UT ({ut_str}) - Flags:\n"
    for line in ut_description:
        description += f"    - {line}\n"

    description += f"  L0 (Sales channel)           : {l0}\n"
    description += f"  AFR                         : {afr}\n"
    description += f"  L1 (Category)                : {l1}\n"
    description += f"  OKNOK (Extra data)           : {oknok}\n"
    description += f"  L5 (Primary data)            : {l5}\n"
    description += f"  L2 (Additional data)         : {l2}\n"
    description += f"  BEL (Receipt Total)          : {bel}\n"

    category_map = {
        "1": "Customer number (SNI)",
        "2": "Requisition number",
        "3": "Customer order",
        "4": "Internet order",
        "5": "Sales order",
        "6": "Vendor order"
    }

    description += "\n  ↪ Category Info:\n"
    category_desc = category_map.get(l1, "Unknown")
    description += f"     - Category                : {category_desc}\n"

    if l1 == "3":  # Customer order
        order_type = {
            "0": "Order start",
            "1": "Order end",
            "2": "Table bill start",
            "3": "Table bill end"
        }.get(oknok, "Unknown")

        price_source = {
            "0": "Order not related to GQ",
            "1": "Non-stock article, price from order",
            "2": "Stock article, price from order",
            "3": "Stock article, price from PLU",
            "4": "Cheapest of order/PLU price",
            "5": "Price from order, no auto discount",
            "6": "Best price calculation on till"
        }.get(l2, "Unknown")

        description += f"     - Order Type             : {order_type}\n"
        description += f"     - Price Source           : {price_source}\n"

    elif l1 == "4":  # Internet order
        eat_type = {
            "0": "Eat In",
            "1": "Take Away"
        }.get(oknok, "Unknown")

        order_source = {
            "0": "Normal order",
            "1": "Hybris order",
            "2": "Matas logic (PLU price from order)"
        }.get(l2, "Unknown")

        description += f"     - Internet Order Type    : {eat_type}\n"
        description += f"     - Order Source           : {order_source}\n"

    elif l1 == "6":  # Vendor order
        invoice_type = {
            "0": "Vendor invoice",
            "1": "Invoice difference",
            "2": "Return to vendor"
        }.get(oknok, "Unknown")
        description += f"     - Vendor Invoice Type    : {invoice_type}\n"

    return description.strip()


def decode_tt34(values: list[str]) -> str:
    if len(values) < 9:
        return "Invalid TT34 input. Expected at least 9 fields."

    _, ut_str, l0, afr, l1, oknok, l5, l2, *bel = values
    bel = " ".join(bel) if bel else "(empty)"

    ut = int(ut_str)

    # No bits defined in docs, but we keep structure in case future flags are added
    ut_description = []
    ut_description.append("(no defined bits for TT34)")

    oknok_map = {
        "0": "Undefined",
        "5": "Refund via GQ",
        "99": "Refund via manual key function"
    }
    oknok_desc = oknok_map.get(oknok, "Unknown")

    description = f"TT34 - Header for article return (format C):\n"
    description += f"  UT ({ut_str}) - Flags:\n"
    for line in ut_description:
        description += f"    - {line}\n"

    description += f"  L0 (Original store number)   : {l0}\n"
    description += f"  AFR (Original line number)   : {afr}\n"
    description += f"  L1 (Original till number)    : {l1}\n"
    description += f"  OKNOK (Refund type)          : {oknok} ({oknok_desc})\n"
    description += f"  L5 (Original receipt number) : {l5}\n"
    description += f"  L2 (Original cashier number) : {l2}\n"
    description += f"  BEL (Original date YYMMDD)   : {bel}\n"

    return description.strip()


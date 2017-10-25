'''Error messages for our tokenizer'''
def bad_token():
    return 'Unexpected character %r on line %d, %s'
def bad_id():
    return "Poorly formed identifer, '%s'. Line %s, %s"
def open_cmnt():
    return 'Non-terminating comment. Line %s, %s'
def cmnt_end():
    return 'Comment end without a beginning. Line %s, %s'
def int_overflow():
    return 'Line %s: Integer value is out of range (0 <= int <= 32767), %s'

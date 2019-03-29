import sys
import csv

def contains_replace_char(value):
    if "\uFFFD" in value:
        return True 
    return False 

def normalize_timestamp(timestamp_string):
    # This is a stub for real logic
    return timestamp_string

def normalize_address(address_string):
    return '\"{}\"'.format(address_string)

def normalize_zip(zip_string):
    # (TODO: validate this is an integer and handle)
    while len(zip_string) < 5:
        zip_string = "0" + zip_string
    return zip_string 

def normalize_name(name_string):
    return name_string.upper()

def normalize_duration(duration_string):
    # This is a stub for real logic
    return duration_string

def calculate_duration(duration1, duration2):
    # This is a stub for real logic
    return duration1 + duration2

def normalize_notes(notes_string):
    return notes_string

def main():
    raw_stdin = sys.stdin.buffer
    rows = raw_stdin.read().split(b'\n')
    for index, row in enumerate(rows):
        utf8_row = row.decode("utf-8", "replace")

        # Avoid choking on empty lines
        if utf8_row == '':
            break

        # This seemed hacky but at the same time regexes make me sad.
        for parsed_row in csv.reader([utf8_row]):

            # Don't process header row just print it
            if index == 0:
                print(utf8_row, file=sys.stdout)
                break

            # (TODO: what if the columns aren't always the same or ordered this way)
            # check for the utf-8 replacement character skipping notes
            if len(list(filter(contains_replace_char,parsed_row[0:6]))) > 0:
                # (TODO: writes to stderr but also stdout at the end of run???)
                sys.stderr.write("WARNING: Could not parse a field in input. Dropped row {}.".format(index+1))
                break

            # (TODO: fix timestamps in parsed_row[0])
            parsed_row[0] = normalize_timestamp(parsed_row[0])
            parsed_row[1] = normalize_address(parsed_row[1])
            parsed_row[2] = normalize_zip(parsed_row[2])
            parsed_row[3] = normalize_name(parsed_row[3])
            parsed_row[4] = normalize_duration(parsed_row[4])
            parsed_row[5] = normalize_duration(parsed_row[5])
            parsed_row[6] = calculate_duration(parsed_row[4], parsed_row[5])
            parsed_row[7] = normalize_notes(parsed_row[7])
            print(",".join(parsed_row), file=sys.stdout)
            
    sys.stdin.close()

if __name__ == '__main__':
    main()

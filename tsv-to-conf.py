import sys
import csv
from datetime import datetime

def convert_tsv_to_geo(tsv_file, geo_file):
    with open(tsv_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(geo_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile, delimiter='\t')
        outfile.write(f"# generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} from {tsv_file}\n")
        outfile.write('geo $blocked_ip {\n')
        outfile.write('\tdefault 0;\n\n')

        for row in reader:
            cidr = row['cidr']
            description = row['description']
            reason = row['reason']

            # Write the CIDR and descriptions to the output file
            if description:
                outfile.write(f'\t# {description.strip()}\n')  # Write description as comment

            if reason and len(reason.strip()) > 1:
                outfile.write(f'\t{cidr} 1; # {reason}\n\n')
            else:
                outfile.write(f'\t{cidr} 1;\n\n')

        outfile.write('}\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert_tsv.py <input.tsv> <output.conf>")
        sys.exit(1)

    convert_tsv_to_geo(sys.argv[1], sys.argv[2])

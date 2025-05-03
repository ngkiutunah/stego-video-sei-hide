def extract_sei_from_h264(file_path, output_file):
    with open(file_path, 'rb') as f:
        data = f.read()

    i = 0
    sei_msgs = []

    while i < len(data) - 4:
        if data[i:i+3] == b'\x00\x00\x01' or data[i:i+4] == b'\x00\x00\x00\x01':
            if data[i:i+4] == b'\x00\x00\x00\x01':
                nal_start = i + 4
                i += 4
            else:
                nal_start = i + 3
                i += 3

            nal_type = data[nal_start] & 0x1F
            if nal_type == 6:  # SEI
                sei_end = data.find(b'\x00\x00\x01', nal_start)
                if sei_end == -1:
                    sei_end = len(data)
                sei_data = data[nal_start+1:sei_end]

                try:
                    text = sei_data.decode('utf-8', errors='ignore')
                    if '[STEGO]' in text:
                        start = text.find('[STEGO]') + len('[STEGO]')
                        message = text[start:].split('\x00')[0].strip()
                        sei_msgs.append(message)
                except Exception as e:
                    continue
        else:
            i += 1

    with open(output_file, 'w') as out_f:
        for msg in sei_msgs:
            out_f.write(msg + '\n')

if __name__ == "__main__":
    extract_sei_from_h264("stego_kitten.h264", "message.txt")

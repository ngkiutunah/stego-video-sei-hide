def create_sei_nal(message):
    start_code = b'\x00\x00\x00\x01'
    nal_header = b'\x06'  # NAL type 6 = SEI
    sei_type = b'\x05'    # user_data_unregistered
    sei_payload = message.encode('utf-8')
    sei_payload_size = bytes([len(sei_payload)])
    rbsp_trailing_bits = b'\x80'

    sei_nal = start_code + nal_header + sei_type + sei_payload_size + sei_payload + rbsp_trailing_bits
    return sei_nal

def insert_sei_safely(original_data, sei_nal):
    i = 0
    positions = []
    while i < len(original_data) - 4:
        if original_data[i:i+4] == b'\x00\x00\x00\x01':
            nal_start = i + 4
            nal_type = original_data[nal_start] & 0x1F
            if nal_type in [5, 7]:  # IDR (5) hoặc SPS (7)
                positions.append(i)
        i += 1

    if positions:
        insert_point = positions[0]  # chèn sau SPS hoặc IDR đầu tiên
        return original_data[:insert_point] + sei_nal + original_data[insert_point:]
    else:
        return sei_nal + original_data  # fallback: chèn vào đầu nếu không tìm được điểm phù hợp

if __name__ == '__main__':
    # Đọc video gốc .h264
    with open("kitten.h264", "rb") as f:
        original = f.read()

    # Tạo SEI chứa thông điệp cần giấu
    message = "[STEGO]Kin Cha Na Sa rang he"
    sei_nal = create_sei_nal(message)

    # Chèn SEI vào vị trí an toàn
    stego_data = insert_sei_safely(original, sei_nal)

    # Ghi ra file mới
    with open("stego_kitten.h264", "wb") as f:
        f.write(stego_data)

    print("✅ Đã chèn SEI vào stego_kitten.h264")

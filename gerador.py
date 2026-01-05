import qrcode
from PIL import Image

# =========================
# FUNÇÃO CRC16-CCITT (PIX)
# =========================
def crc16(payload):
    crc = 0xFFFF
    polinomio = 0x1021

    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1
            crc &= 0xFFFF

    return format(crc, '04X')


# =========================
# DADOS DO PIX
# =========================
chave_pix = "1c0ba67a-340c-4ed9-b7cc-abdcaba60de8"
nome_recebedor = "Davi"
cidade = "RIO DE JANEIRO"

# =========================
# CAMPO 26 (Merchant Account Information)
# =========================
gui = "br.gov.bcb.pix"
campo_gui = f"0014{gui}"
campo_chave = f"01{len(chave_pix):02d}{chave_pix}"
campo_26 = f"26{len(campo_gui + campo_chave):02d}{campo_gui}{campo_chave}"

# =========================
# MONTAGEM DO PAYLOAD
# =========================
payload = (
    "000201"              # Payload Format Indicator
    + campo_26             # Merchant Account Info
    + "52040000"           # MCC (0000)
    + "5303986"            # Moeda (BRL)
    + "5802BR"             # País
    + f"59{len(nome_recebedor):02d}{nome_recebedor}"
    + f"60{len(cidade):02d}{cidade}"
    + "62070503***"        # TXID
)

# =========================
# CRC16
# =========================
payload_crc = payload + "6304"
payload_crc += crc16(payload_crc)

# =========================
# GERA QR CODE
# =========================
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=16,
    border=4,
)

qr.add_data(payload_crc)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

# Fundo transparente
pixels = img.getdata()
new_pixels = []

for p in pixels:
    if p[0] == 255 and p[1] == 255 and p[2] == 255:
        new_pixels.append((255, 255, 255, 0))
    else:
        new_pixels.append(p)

img.putdata(new_pixels)
img.save("pix_qrcode.png")

print("QR Code Pix gerado com sucesso!")

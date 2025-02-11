from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

def generate_nft_image(message, image_url):
    try:
        # 既存画像を開く
        base_image = Image.open(image_url)

        # 画像の上にテキストを追加
        draw = ImageDraw.Draw(base_image)
        font = ImageFont.load_default()
        text = f"GIFT: {message}"
        draw.text((10, 10), text, font=font, fill="white")

        # QRコードの生成
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, border=4,
        )
        qr.add_data(message)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        base_image.paste(qr_image, (base_image.width - 150, base_image.height - 150))

        # 保存
        output_path = f"output/{message}.png"
        os.makedirs(os.path.dirname(output_path), exit_ok=True)
        base_image.save(output_path)

        # メタデータ
        metadata = {
            "message": message,
            "image_url": image_url,
            "output_path": output_path,
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "invalid arguments"}))
        sys.exit(1)

    message = sys.argv[1]
    image_url = sys.argv[2]
    result = generate_image(message, image_url)
    print(json.dumps(result))
import qrcode
features=qrcode.QRCode(version=1, box_size=40, border=3)
features.add_data("https://docs.python.org/3/library/venv.html")
features.make(fit=True)
#gen_img=qrcode.make("QRCode")
gen_img=features.make_image(fill_color="blue", back_color="white")
gen_img.save('image6.png') #to save generaated img

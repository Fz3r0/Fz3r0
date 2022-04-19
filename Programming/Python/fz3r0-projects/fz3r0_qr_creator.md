```python

import io
import qrcode

qr = qrcode.QRCode()
qr.add_data("I'm fz3r0, and the sun no loger rises...")
f = io.StringIO()
qr.print_ascii(out=f)
f.seek(0)
print(f.read())

```

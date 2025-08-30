# BookingMovie - Hướng dẫn chạy trên mạng LAN (client-server)

Mục tiêu: chạy ứng dụng Flask trên một máy (server) và truy cập từ các máy khác trong cùng mạng nội bộ (LAN).

Các bước nhanh:

1) Cài dependencies (trên máy server)

```powershell
cd C:\Users\Admin\Desktop\bookingmovieee
python -m pip install -r requirements.txt
```

2) Mở firewall Windows cho cổng (mặc định 5000) nếu cần. Bạn có thể tạm thời cho phép qua PowerShell (quyền Admin):

```powershell
New-NetFirewallRule -DisplayName "Allow Flask 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

3) Khởi động server:

```powershell
# Chạy ở dạng debug (mặc định)
python app.py
# Hoặc gán host/port qua biến môi trường
$env:FLASK_RUN_HOST = '0.0.0.0'; $env:FLASK_RUN_PORT = '5000'; python app.py
```

Khi server khởi động, README sẽ in địa chỉ LAN ví dụ `http://192.168.1.10:5000`.

4) Trên máy client (cùng mạng), mở trình duyệt và truy cập địa chỉ LAN đó.

Ghi chú kỹ thuật và lưu ý bảo mật:

- Ứng dụng đang dùng SQLite (`movies.db`). Khi chạy kiểu client-server, chỉ chạy server trên một máy, các client truy cập qua HTTP. Database nằm trên server; không copy file sqlite tới nhiều máy.
- Trong môi trường sản xuất: dùng WSGI server (Gunicorn, uWSGI) hoặc deploy qua Docker/nginx, và bật HTTPS.
- Cân nhắc hash mật khẩu (hiện tại mật khẩu lưu thô) bằng `werkzeug.security.generate_password_hash` và `check_password_hash`.
- Nếu máy chủ có nhiều interface hoặc VPN, đảm bảo sử dụng IP nội bộ đúng (ipconfig / ifconfig) để truy cập từ client.

Thêm tính năng nếu cần:
- Tạo Dockerfile để deploy dễ dàng trên nhiều máy.
- Chuyển SQLite -> PostgreSQL cho nhiều kết nối đồng thời.
- Sinh HTTPS tự động với Let's Encrypt (qua reverse proxy nginx).

Background image
----------------
Đặt file ảnh nền vào `static/images/` và đặt tên `bg.jpg` (hoặc sửa đường dẫn trong `static/css/style.css` ở lớp `.page-bg`). Trang chủ và trang admin đã dùng lớp `.page-bg` để hiển thị ảnh nền.


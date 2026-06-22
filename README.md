# Book Management

Ứng dụng quản lý sách gồm Django REST Framework và React/Vite. Chức năng chính: JWT login/refresh/logout, CRUD sách, lọc, phân trang theo `page` và `page_size`, cùng trạng thái loading cho các thao tác gọi API.

## Chạy backend

Tạo `backend/.env` với cấu hình MySQL (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) rồi chạy:

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Để dùng SQLite khi phát triển hoặc test, đặt `DB_ENGINE=django.db.backends.sqlite3` và `DB_NAME=db.sqlite3`.

## Chạy frontend

```bash
cd frontend
npm ci
npm run dev
```

Nếu frontend và backend chạy khác origin, đặt `VITE_API_URL=http://127.0.0.1:8000/api` trong `frontend/.env`.

## Kiểm tra

```bash
cd backend && python manage.py test
cd frontend && npm run lint && npm run build
```

Ví dụ phân trang: `/api/books/?page=2&page_size=20`. Trang React cũng lưu `page` và `page_size` trên URL để có thể tải lại hoặc chia sẻ đúng trang hiện tại.

# V60 XSMB - Web Soi Cầu Tự Động

Web: https://letiencung.github.io/v60-xsmb/

## Mô tả

Giao diện phân tích xổ số miền Bắc (V60) chạy trên web, **tự động cập nhật số liệu mới nhất mỗi ngày** mà người dùng không cần làm gì.

## Cách hoạt động

| File | Vai trò |
|------|---------|
| `index.html` | Giao diện V60. Khi mở trang, tự tải `data.json` mới nhất |
| `data.json` | Số liệu 7 ngày gần nhất (định dạng JSON) |
| `fetch_data.py` | Script tải số liệu từ xosodaiphat.com |
| `.github/workflows/update-data.yml` | Lịch tự động chạy mỗi tối 18:32 |

## Lịch tự động

Mỗi tối lúc **18:32** (giờ Việt Nam), GitHub Actions tự động:
1. Tải kết quả XSMB mới nhất từ xosodaiphat.com
2. Cập nhật `data.json`
3. Web tự có số mới — người dùng chỉ việc mở link

## Cho người dùng cuối

Mở link web trên điện thoại → bấm ⋮ → **Thêm vào Màn hình chính**.
Từ nay bấm biểu tượng là xem, như app, lúc nào cũng số mới nhất.

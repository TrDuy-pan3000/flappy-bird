# 🚀 Hướng dẫn Deploy Flappy Bird lên GitHub Pages

## Bước 1: Tạo Repository trên GitHub

1. Truy cập https://github.com và đăng nhập
2. Click nút **"New"** hoặc **"+"** ở góc trên bên phải
3. Chọn **"New repository"**
4. Điền thông tin:
   - **Repository name**: `flappy-bird` (hoặc tên bạn muốn)
   - **Description**: "A feature-rich Flappy Bird game with mini-games"
   - Chọn **Public** (để có thể deploy lên GitHub Pages miễn phí)
   - **KHÔNG** chọn "Initialize with README" (vì đã có sẵn)
5. Click **"Create repository"**

## Bước 2: Push code lên GitHub

Sau khi tạo repository, GitHub sẽ hiển thị hướng dẫn. Sử dụng lệnh sau:

```bash
# Thêm remote repository (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/flappy-bird.git

# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

**Lưu ý**: Nếu được yêu cầu đăng nhập, sử dụng **Personal Access Token** thay vì mật khẩu:
- Vào Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token với quyền `repo`
- Sử dụng token này làm mật khẩu khi push

## Bước 3: Cấu hình GitHub Pages

1. Vào repository trên GitHub
2. Click tab **"Settings"**
3. Ở menu bên trái, click **"Pages"**
4. Trong phần **"Source"**, chọn:
   - Source: **GitHub Actions**
5. Click **"Save"**

## Bước 4: Kích hoạt GitHub Actions

1. Vào tab **"Actions"** trong repository
2. Nếu được hỏi, click **"I understand my workflows, go ahead and enable them"**
3. Workflow sẽ tự động chạy sau khi push code

## Bước 5: Chờ deployment hoàn tất

1. Vào tab **"Actions"** để xem tiến trình
2. Click vào workflow đang chạy để xem chi tiết
3. Đợi cho đến khi cả 2 jobs (build và deploy) hoàn thành (có dấu ✓ xanh)
4. Thời gian build khoảng 2-5 phút

## Bước 6: Truy cập game

Sau khi deployment hoàn tất, game sẽ có sẵn tại:

```
https://YOUR_USERNAME.github.io/flappy-bird/
```

(Thay YOUR_USERNAME bằng username GitHub của bạn)

## ⚠️ Lưu ý quan trọng

### Về Pygbag và Web Deployment

Game này được chuyển đổi để chạy trên web bằng **Pygbag**. Tuy nhiên, có một số hạn chế:

1. **Không phải tất cả tính năng Pygame đều hoạt động trên web**
2. **Assets (hình ảnh, âm thanh) cần được load đúng cách**
3. **Performance có thể khác so với chạy local**

### Nếu gặp lỗi khi build

Nếu GitHub Actions báo lỗi, có thể do:

1. **Thiếu assets**: Đảm bảo thư mục `assets/` có đầy đủ file
2. **Import lỗi**: Một số module có thể không tương thích với web
3. **File paths**: Pygbag yêu cầu relative paths

### Giải pháp thay thế

Nếu Pygbag không hoạt động tốt, bạn có thể:

1. **Deploy video demo**: Tạo video gameplay và host trên GitHub Pages
2. **Chỉ share code**: Người dùng tải về và chạy local
3. **Sử dụng Replit**: Deploy trên Replit.com (dễ hơn cho Pygame)

## 🔄 Cập nhật game sau này

Khi muốn cập nhật game:

```bash
# Sau khi sửa code
git add .
git commit -m "Mô tả thay đổi"
git push
```

GitHub Actions sẽ tự động build và deploy lại!

## 📝 Checklist

- [ ] Tạo repository trên GitHub
- [ ] Push code lên GitHub
- [ ] Enable GitHub Pages với source là GitHub Actions
- [ ] Chờ workflow chạy xong
- [ ] Truy cập URL để test game
- [ ] Cập nhật README.md với link game (nếu muốn)

## 🆘 Cần trợ giúp?

Nếu gặp vấn đề:
1. Check tab Actions để xem lỗi cụ thể
2. Đọc logs của workflow
3. Có thể cần điều chỉnh code để tương thích với Pygbag

---

**Chúc bạn deploy thành công! 🎮🚀**

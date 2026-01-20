# 🚀 HƯỚNG DẪN NHANH - PUSH LÊN GITHUB

## Cách 1: Sử dụng Script Tự Động (Đơn giản nhất) ⭐

### Bước 1: Tạo Repository trên GitHub

1. Mở trình duyệt và vào: **https://github.com/new**
2. Đăng nhập nếu chưa đăng nhập
3. Điền thông tin:
   - **Repository name**: `flappy-bird` (hoặc tên bạn muốn)
   - **Description**: "Flappy Bird game with mini-games"
   - Chọn **Public**
   - **KHÔNG** tick "Add a README file"
4. Click **"Create repository"**

### Bước 2: Chạy Script

Mở PowerShell trong thư mục này và chạy:

```powershell
.\push_to_github.ps1
```

Script sẽ hỏi:
- **GitHub Username**: Nhập username GitHub của bạn
- **Repository Name**: Nhập tên repository vừa tạo (ví dụ: `flappy-bird`)

Sau đó script sẽ tự động push code lên GitHub!

### Bước 3: Cấu hình GitHub Pages

1. Vào repository trên GitHub
2. Click tab **"Settings"**
3. Click **"Pages"** ở menu bên trái
4. Trong **"Source"**, chọn: **GitHub Actions**
5. Vào tab **"Actions"** để xem tiến trình build

### Bước 4: Chờ và Truy cập

- Đợi 2-5 phút để GitHub Actions build xong
- Game sẽ có tại: `https://YOUR_USERNAME.github.io/flappy-bird/`

---

## Cách 2: Chạy Lệnh Thủ Công

Nếu không muốn dùng script, chạy các lệnh sau:

```powershell
# Thay YOUR_USERNAME và REPO_NAME bằng thông tin của bạn
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Lưu Ý Quan Trọng

### Nếu bị yêu cầu đăng nhập khi push:

GitHub không còn cho phép dùng mật khẩu. Bạn cần **Personal Access Token**:

1. Vào: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Đặt tên token (ví dụ: "Flappy Bird Deploy")
4. Chọn quyền: **repo** (tick vào ô repo)
5. Click **"Generate token"**
6. **COPY TOKEN NGAY** (chỉ hiện 1 lần!)
7. Khi push, dùng token này làm **mật khẩu**

### Nếu gặp lỗi "repository not found":

- Kiểm tra lại tên repository
- Đảm bảo repository đã được tạo trên GitHub
- Kiểm tra username có đúng không

---

## 📋 Checklist Nhanh

- [ ] Tạo repository trên GitHub (Public, không tick README)
- [ ] Chạy `.\push_to_github.ps1` hoặc lệnh git thủ công
- [ ] Vào Settings → Pages → chọn GitHub Actions
- [ ] Chờ Actions chạy xong (tab Actions)
- [ ] Truy cập game tại `https://USERNAME.github.io/REPO_NAME/`

---

## 🆘 Cần Trợ Giúp?

Xem file **DEPLOY_GUIDE.md** để có hướng dẫn chi tiết hơn!

---

**Chúc bạn thành công! 🎮**

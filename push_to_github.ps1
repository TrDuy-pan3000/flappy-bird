# Script để push Flappy Bird lên GitHub
# Chạy script này sau khi đã tạo repository trên GitHub

Write-Host "=== PUSH FLAPPY BIRD LÊN GITHUB ===" -ForegroundColor Cyan
Write-Host ""

# Yêu cầu nhập thông tin
Write-Host "Vui lòng nhập thông tin GitHub của bạn:" -ForegroundColor Yellow
Write-Host ""

$username = Read-Host "GitHub Username"
$repoName = Read-Host "Repository Name (ví dụ: flappy-bird)"

Write-Host ""
Write-Host "Đang cấu hình Git..." -ForegroundColor Green

# Kiểm tra xem đã có remote chưa
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote 'origin' đã tồn tại. Đang xóa..." -ForegroundColor Yellow
    git remote remove origin
}

# Thêm remote mới
$repoUrl = "https://github.com/$username/$repoName.git"
Write-Host "Đang thêm remote: $repoUrl" -ForegroundColor Green
git remote add origin $repoUrl

# Đổi tên branch thành main
Write-Host "Đang đổi tên branch thành 'main'..." -ForegroundColor Green
git branch -M main

# Push lên GitHub
Write-Host ""
Write-Host "Đang push code lên GitHub..." -ForegroundColor Green
Write-Host "Lưu ý: Nếu được yêu cầu đăng nhập, sử dụng Personal Access Token thay vì mật khẩu!" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== PUSH THÀNH CÔNG! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Các bước tiếp theo:" -ForegroundColor Cyan
    Write-Host "1. Vào https://github.com/$username/$repoName" -ForegroundColor White
    Write-Host "2. Click tab 'Settings'" -ForegroundColor White
    Write-Host "3. Click 'Pages' ở menu bên trái" -ForegroundColor White
    Write-Host "4. Trong 'Source', chọn 'GitHub Actions'" -ForegroundColor White
    Write-Host "5. Vào tab 'Actions' để xem tiến trình build" -ForegroundColor White
    Write-Host "6. Sau khi build xong, game sẽ có tại:" -ForegroundColor White
    Write-Host "   https://$username.github.io/$repoName/" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=== CÓ LỖI XẢY RA ===" -ForegroundColor Red
    Write-Host ""
    Write-Host "Các nguyên nhân có thể:" -ForegroundColor Yellow
    Write-Host "1. Repository chưa được tạo trên GitHub" -ForegroundColor White
    Write-Host "2. Sai username hoặc repository name" -ForegroundColor White
    Write-Host "3. Chưa đăng nhập hoặc không có quyền truy cập" -ForegroundColor White
    Write-Host ""
    Write-Host "Hướng dẫn tạo Personal Access Token:" -ForegroundColor Cyan
    Write-Host "1. Vào https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Click 'Generate new token' -> 'Generate new token (classic)'" -ForegroundColor White
    Write-Host "3. Chọn quyền 'repo'" -ForegroundColor White
    Write-Host "4. Copy token và sử dụng làm mật khẩu khi push" -ForegroundColor White
    Write-Host ""
}

Write-Host "Nhấn Enter để đóng..." -ForegroundColor Gray
Read-Host

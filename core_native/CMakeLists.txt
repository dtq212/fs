cmake_minimum_required(VERSION 3.22)

# Tên project và ngôn ngữ sử dụng
project(autofarm_native LANGUAGES CXX)

# Thiết lập chuẩn C++17 (NDK r27d hỗ trợ rất tốt)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Khai báo tạo file thư viện dùng chung (.so)
add_library(autofarm_core SHARED autofarm_core.cpp)

# Liên kết với thư viện log của Android để bạn có thể xem kết quả qua Logcat
target_link_libraries(autofarm_core log)
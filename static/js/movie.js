document.addEventListener("DOMContentLoaded", function() {
    // Lấy tất cả các ghế
    const seats = document.querySelectorAll("input[name='seats']");
    const selectedSeats = []; // Mảng lưu trữ các ghế đã chọn

    // Lặp qua tất cả các ghế và xử lý sự kiện thay đổi (chọn hoặc bỏ chọn ghế)
    seats.forEach(seat => {
        seat.addEventListener("change", function() {
            if (seat.checked) {
                // Thêm ghế vào mảng khi người dùng chọn
                selectedSeats.push(seat.value);
            } else {
                // Xoá ghế khỏi mảng khi người dùng bỏ chọn
                const index = selectedSeats.indexOf(seat.value);
                if (index > -1) selectedSeats.splice(index, 1);
            }
        });
    });

    // Khi người dùng nhấn nút Đặt vé
    document.querySelector("form").addEventListener("submit", function(event) {
        event.preventDefault();  // Ngừng gửi form mặc định

        if (selectedSeats.length > 0) {
            // Gửi yêu cầu POST với danh sách ghế đã chọn
            fetch(`/movie/{{ movie.id }}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    seats: selectedSeats
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Booking successful") {
                    alert("Đặt vé thành công!");
                    // Cập nhật lại giao diện, đánh dấu ghế đã đặt
                    selectedSeats.forEach(seatId => {
                        const seatElement = document.querySelector(`input[value='${seatId}']`);
                        if (seatElement) {
                            seatElement.disabled = true;
                            seatElement.parentElement.style.color = 'gray';
                        }
                    });
                } else {
                    alert("Đặt vé thất bại, vui lòng thử lại!");
                }
            })
            .catch(error => {
                console.error("Lỗi khi đặt vé:", error);
                alert("Có lỗi xảy ra, vui lòng thử lại!");
            });
        } else {
            alert("Vui lòng chọn ít nhất một ghế!");
        }
    });
});

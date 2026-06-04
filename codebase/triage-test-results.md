# Triage Test Results

Kết quả chạy tay từng case trong `sample-questions.md` qua prototype đang chạy.

| # | Input | Expected route | Actual route | Safety gate | Pass? | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | Paracetamol 500mg tác dụng gì? | factual | factual | false | ✅ | Disclaimer có |
| 2 | Thuốc Ibuprofen có tác dụng phụ không? | factual | factual | false | ✅ | |
| 3 | Vitamin C uống liều bao nhiêu? | factual | factual | false | ✅ | |
| 4 | Thuốc ho Bảo Thanh thành phần có gì? | factual | factual | false | ✅ | |
| 5 | Panadol và Tylenol có khác nhau không? | factual | factual | false | ✅ | |
| 6 | Thuốc này uống được không? | advisory_gather | advisory_gather | false | ✅ | AI hỏi thêm tên thuốc |
| 7 | Tôi muốn mua thuốc giảm đau, loại nào tốt? | advisory_gather | advisory_gather | false | ✅ | |
| 8 | Con tôi 3 tuổi bị ho, dùng thuốc gì? | advisory_gather | advisory_gather | false | ✅ | |
| 9 | Tôi hay bị đau dạ dày, uống Ibuprofen được không? | advisory_gather | advisory_gather | false | ✅ | |
| 10 | Tôi đang uống thuốc huyết áp, có dùng thêm được không? | advisory_handoff (safety) | advisory_handoff | true | ✅ | "huyết áp" + "đang uống" triggered |
| 11 | Tôi tiểu đường type 2 có dùng Ibuprofen được không? | advisory_handoff (safety) | advisory_handoff | true | ✅ | "tiểu đường" triggered |
| 12 | Đang mang thai 3 tháng, uống Vitamin B được không? | advisory_handoff (safety) | advisory_handoff | true | ✅ | "mang thai" triggered |
| 13 | Tôi đang điều trị ung thư, có uống thêm vitamin được không? | advisory_handoff (safety) | advisory_handoff | true | ✅ | "đang điều trị" triggered |
| 14 | Thuốc bị quá hạn 1 tuần còn dùng được không? | advisory_gather | advisory_gather | false | ✅ | |
| 15 | Uống quá liều Paracetamol thì phải làm gì? | advisory_handoff (safety) | advisory_handoff | true | ✅ | "quá liều" triggered |

**Kết quả: 15/15 pass.**

---

## Error path test

| Scenario | Expected | Actual | Pass? |
|---|---|---|---|
| Backend stopped, gửi tin | UI hiện "❌ Mất kết nối backend" | ✅ st.error hiện đúng | ✅ |
| API key sai / quota hết | Graceful fallback, không 500 | ✅ fallback route trả về | ✅ |

---

## Screenshots

Screenshots lưu tại `evidence/` (chụp trong quá trình test thực tế).

- `evidence/happy-factual-paracetamol.png` — demo câu factual
- `evidence/gather-context-request.png` — demo advisory gather
- `evidence/force-route-tieu-duong.png` — demo safety gate triggered
- `evidence/error-path-backend-down.png` — demo error path

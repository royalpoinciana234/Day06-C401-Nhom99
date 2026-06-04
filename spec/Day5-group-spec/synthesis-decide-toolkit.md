# Toolkit — Từ Evidence Đến Build Slice

Dùng sau khi nhóm đã có evidence. Mục tiêu là chốt một build slice đủ nhỏ cho Day 06.

## 1. Gom evidence thành cụm

Gom theo **workflow/pain**, không gom theo tên feature.

| Cụm pain | Evidence gom vào |
|---|---|
| **Chờ lâu cho câu hỏi đơn giản** | Self-use: "Paracetamol tác dụng gì" chờ 3-5 phút; user bypass chat ra quầy |
| **Dược sĩ quá tải với câu dễ** | Câu factual và câu tư vấn phức tạp chung một hàng chờ — dược sĩ bị chiếm |
| **Gather context thủ công mỗi lần** | Dược sĩ phải hỏi lại từ đầu; user phải giải thích lại dù đã nhắn nhiều tin |
| **Câu phức tạp cũng chờ lâu** | Self-use: câu tương tác thuốc chờ 8 phút — đúng cần người thật nhưng chờ quá lâu |

→ **Root cause:** Long Châu không phân biệt loại câu hỏi → mọi thứ đều vào queue dược sĩ → dược sĩ chậm, user bỏ.

## 2. Viết insight

```text
Khách hàng Long Châu hỏi về thuốc qua chat không chỉ cần được trả lời đúng.
Họ thật ra cần được trả lời nhanh — câu đơn giản trong vài giây, câu khó vào tay dược sĩ không bị chờ hàng —
vì hiện tại không có bước triage nào: câu "Paracetamol là gì" và câu "Tôi đang uống huyết áp
có dùng được Ibuprofen không" xử lý như nhau, gây quá tải và chờ đợi không cần thiết.
```

## 3. Viết opportunity

```text
Cơ hội là thêm AI làm trung gian trong chat Long Châu hiện có:
AI tự trả lời câu hỏi factual ngay lập tức (tác dụng thuốc, thành phần, cách dùng chung),
tự gather context (thuốc đang dùng, triệu chứng, lý do hỏi) trước khi route,
rồi chuyển sang dược sĩ kèm tóm tắt sẵn, dược sĩ tư vấn ngay, không hỏi lại từ đầu,
trong khi kiểm soát failure "AI trả lời câu cần tư vấn cá nhân" bằng rule triage rõ ràng.
```

## 4. Chọn build slice

**Build slice được chọn:**

```text
Cho khách hàng Long Châu đang nhắn tin hỏi về thuốc,
AI làm trung gian: phân loại câu hỏi ngay khi nhận —
  • Factual (tác dụng, thành phần, liều chung) → AI trả lời ngay, không qua dược sĩ
  • Advisory (tư vấn chọn thuốc, tương tác, liều cho bệnh cụ thể) → AI hỏi thêm 1-2 câu context
    rồi route sang dược sĩ kèm tóm tắt: "Khách hỏi X, đang dùng Y, cần tư vấn Z"
Dược sĩ nhảy vào tư vấn ngay, không đọc lại từ đầu.
```

**Kiểm tra 5 câu:**

| Câu hỏi | Đánh giá |
|---|---|
| User cụ thể chưa? | ✅ Khách hàng Long Châu đang dùng tính năng chat, hỏi về thuốc đang mua hoặc định mua |
| Task đủ hẹp chưa? | ✅ Chỉ 1 flow: nhận tin → classify → trả lời hoặc gather+route. Demo được trong 3-4 phút |
| AI decision rõ chưa? | ✅ AI quyết định: câu này tôi trả lời được, hay tôi cần route? Rule phân loại explicit |
| Failure path rõ chưa? | ✅ AI classify nhầm câu advisory thành factual → trả lời thiếu context → sai |
| Có evidence không? | ✅ Self-use Long Châu chat (2 obs) + phỏng vấn nhanh (2 cases) |

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định nhóm |
|---|---|
| Evidence yếu, user mơ hồ | Không áp dụng |
| Ý tưởng quá rộng | **Áp dụng:** chỉ build triage + 2 path (trả lời / route). Không build quản lý lịch sử chat, không build dashboard dược sĩ |
| AI không cần thiết | Không áp dụng — classification và context gathering là core AI task |
| Rủi ro cao | **Áp dụng:** câu advisory luôn route người thật, không để AI tự tư vấn |
| Không demo được trong 1 ngày | Không áp dụng — 1 prompt classifier + 2 response handler = khả thi |

## 6. Câu chốt cuối

```text
Dựa trên evidence (tự dùng thử chat Long Châu chờ 3-8 phút + phỏng vấn người dùng bỏ qua kênh chat),
nhóm sẽ build AI middleware layer cho chat Long Châu:
  tự trả lời câu factual ngay lập tức,
  gather context và route câu advisory sang dược sĩ kèm tóm tắt sẵn,
cho khách hàng đang nhắn tin hỏi về thuốc,
để giải quyết pain "chờ lâu cho câu đơn giản + dược sĩ quá tải",
và sẽ test failure path: AI classify nhầm câu tương tác thuốc thành factual → trả lời thiếu context.
```

## 7. Backlog

Những thứ **không build trong Day 06**:

- Dashboard cho dược sĩ theo dõi queue
- Lưu lịch sử câu hỏi của từng khách
- AI học từ câu trả lời của dược sĩ để cải thiện
- Tích hợp với hệ thống POS/đơn thuốc Long Châu
- Hỗ trợ hình ảnh (user gửi ảnh thuốc để hỏi)

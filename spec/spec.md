# SPEC – AI Triage for Long Châu Pharmacy Chat

## 1. Bằng chứng

### Evidence 1 – Trải nghiệm trực tiếp

Nhóm sử dụng tính năng chat tư vấn của Long Châu để hỏi:

> "Thuốc Nano Fucoidan Biochempha có tác dụng gì?"

Kết quả:

* Mất khoảng 3–5 phút mới nhận được phản hồi.
* Câu hỏi chỉ mang tính tra cứu thông tin đơn giản nhưng vẫn phải vào hàng chờ dược sĩ.

**Nhận định:**

* Nhiều câu hỏi chỉ yêu cầu tra cứu thông tin cơ bản về thuốc (công dụng, thành phần, cách bảo quản) nhưng vẫn phải chờ dược sĩ phản hồi.
* Người dùng phải chờ dù hoàn toàn có thể nhận được câu trả lời ngay.

---

### Evidence 2 – Phỏng vấn nhanh người dùng

Người dùng cho biết:

> "Nếu chat không có phản hồi nhanh thì tôi thường ra trực tiếp nhà thuốc hoặc gọi điện."

Kết quả: 
* Người dùng không tiếp tục chờ trên kênh chat khi thời gian phản hồi quá lâu.
* Người dùng chuyển sang các kênh hỗ trợ khác như gọi điện hoặc đến trực tiếp nhà thuốc để được tư vấn.

**Nhận định:**

* Người dùng cần nhận được phản hồi trong thời gian ngắn khi sử dụng kênh chat tư vấn.
* Các câu hỏi đơn giản cần được xử lý nhanh hơn để giảm thời gian chờ và giữ người dùng ở lại trên kênh chat.
* Việc thiếu phản hồi kịp thời làm giảm hiệu quả của kênh chat trong việc hỗ trợ người dùng.

---

### Evidence 3 – Trải nghiệm trực tiếp với câu hỏi chuyên môn

Nhóm thử hỏi:

> "Tôi đang dùng thuốc A, có uống thêm thuốc B được không?"

Kết quả:

* Chờ khoảng 8 phút.
* Dược sĩ trả lời chính xác nhưng phải hỏi lại nhiều thông tin từ đầu.

**Nhận định:**

* Những câu hỏi advisory cần dược sĩ thật.
* Vấn đề nằm ở việc thu thập context thủ công và thời gian chờ.

---

### Các giả định còn chưa được kiểm chứng

* Tỷ lệ câu hỏi factual trong tổng số câu hỏi chat lớn hơn 40%.
* Người dùng sẵn sàng tương tác với AI nếu biết cuối cùng vẫn có dược sĩ hỗ trợ.

Các giả định này sẽ được kiểm chứng bằng dữ liệu test và phỏng vấn thêm trong giai đoạn tiếp theo.

---

## 2. Lát cắt để build

### Một người dùng

Khách hàng Long Châu đang chat để hỏi về thuốc.

### Một công việc

Tìm hiểu thông tin thuốc hoặc xin tư vấn sử dụng thuốc.

### Một quyết định AI

Phân loại câu hỏi thành:

* Factual (tra cứu thông tin):
Là các câu hỏi có câu trả lời tương đối cố định, không phụ thuộc vào tình trạng cụ thể của người hỏi.
* Advisory (tư vấn cá nhân hóa):
Là các câu hỏi cần xem xét thông tin cụ thể của người dùng trước khi trả lời.

### Một kết quả trả về

* Trả lời ngay bằng AI.
* Hoặc chuyển sang dược sĩ kèm context đã được tóm tắt.

---

## 3. AI Product Canvas

### Value – Giá trị

**Đối tượng:**

* Khách hàng Long Châu hỏi thông tin thuốc.
* Phụ huynh hỏi thuốc cho con.
* Người có bệnh nền cần tư vấn sử dụng thuốc.

**Nỗi đau hiện tại:**

* Chờ 3–8 phút cho mọi loại câu hỏi.
* Dược sĩ phải hỏi lại context nhiều lần.
* Người dùng bỏ kênh chat khi không được phản hồi nhanh.

**Giá trị AI mang lại:**

* Trả lời ngay các câu hỏi factual.
* Thu thập context trước khi chuyển dược sĩ.
* Giảm thời gian xử lý của dược sĩ.

---

### Trust – Niềm tin

Nếu AI trả lời sai:

* Người dùng có nút "Trao đổi với dược sĩ".
* Tất cả câu trả lời AI đều kèm disclaimer:

> "Thông tin chỉ mang tính tham khảo. Nếu bạn đang điều trị bệnh hoặc sử dụng thuốc theo đơn, hãy trao đổi với dược sĩ để được tư vấn chính xác."

* Các câu có dấu hiệu rủi ro sẽ tự động chuyển sang dược sĩ.

---

### Feasibility – Tính khả thi

**Chi phí:**

* 1 lần gọi AI cho classifier.
* 1 lần gọi AI cho response hoặc handoff summary.

**Độ trễ mục tiêu:**

* < 3 giây cho factual.
* < 5 giây cho advisory routing.

**Dữ liệu cần có:**

* Danh sách thuốc phổ biến.
* Bộ test factual/advisory.
* Danh sách từ khóa rủi ro.

**Rủi ro lớn nhất:**

* Classify sai câu advisory thành factual.

**Điều kiện dừng:**

* Accuracy classifier dưới 80%.
* Tỷ lệ route sai vượt quá 10%.

---

### Tín hiệu học

Khi người dùng:

* Bấm "Trao đổi với dược sĩ"
* Sửa thông tin
* Không hài lòng với câu trả lời AI

Hệ thống lưu:

```text
Question
AI Classification
AI Response
User Correction
Final Pharmacist Response
```

Dữ liệu này được dùng để:

* Cập nhật test cases.
* Cải thiện prompt classifier.
* Cải thiện keyword trigger.

---

## 4. Tăng năng lực hay tự động hóa

### Lựa chọn

**Conditional Automation**

### AI tự động thực hiện

* Phân loại câu hỏi.
* Trả lời factual.
* Thu thập context.
* Tạo handoff summary.

### Con người quyết định

* Dược sĩ quyết định với mọi câu hỏi advisory.
* Người dùng quyết định có tiếp tục hỏi dược sĩ hay không.

### Lý do

Sai sót trong tư vấn thuốc có thể ảnh hưởng trực tiếp đến sức khỏe người dùng. Vì vậy AI chỉ được tự động hóa ở các trường hợp rủi ro thấp và phải chuyển cho dược sĩ ở các trường hợp cần đánh giá cá nhân.

---

## 5. Bốn đường đi của trải nghiệm

| Đường đi | Tình huống | Hệ thống xử lý |
|-----------|-----------|-----------|
| **Đường thuận (Happy Path)** | User hỏi: "Paracetamol 500mg có tác dụng gì?" | AI classify là **Factual** và trả lời ngay trong dưới 3 giây kèm disclaimer. |
| **Khi AI không chắc (Low Confidence)** | User hỏi: "Thuốc này uống được không?" | AI không đủ thông tin để phân loại nên hỏi thêm: "Bạn đang hỏi về thuốc nào?" hoặc "Bạn có đang dùng thuốc khác không?" |
| **Khi AI sai / có rủi ro (Failure Path)** | User hỏi: "Tôi bị tiểu đường type 2 có dùng được Ibuprofen không?" | AI nhận diện đây là câu hỏi **Advisory**, không tự trả lời mà hỏi thêm context rồi tạo handoff summary và chuyển sang dược sĩ. |
| **Khi người dùng sửa (Correction Path)** | User phát hiện AI hiểu sai hoặc dược sĩ nhận thấy summary chưa chính xác. | Dược sĩ chỉnh sửa summary và trả lời trực tiếp. Hệ thống lưu lại correction để cải thiện prompt và test cases sau này. |
---

## 6. Những kiểu lỗi đáng lo nhất

### Lỗi 1 – Classify sai Advisory thành Factual

**Xuất hiện khi:**

* Có bệnh nền nhưng AI không nhận diện.
* User mô tả mơ hồ.

**Ảnh hưởng:**

* Người dùng nhận tư vấn không phù hợp.
* Rủi ro sức khỏe cao.

**Xử lý:**

* Keyword trigger bắt buộc route.
* Disclaimer bắt buộc trên mọi câu trả lời AI.

---

### Lỗi 2 – Tóm tắt context sai

**Xuất hiện khi:**

* AI bỏ sót thông tin quan trọng.

**Ảnh hưởng:**

* Dược sĩ mất thêm thời gian xác minh.

**Xử lý:**

* Hiển thị lịch sử chat đầy đủ.
* Dược sĩ có quyền chỉnh sửa summary.

---

### Lỗi 3 – Hallucination thông tin thuốc

**Xuất hiện khi:**

* AI trả lời ngoài phạm vi dữ liệu.

**Ảnh hưởng:**

* User tin vào thông tin sai.

**Xử lý:**

* Giới hạn phạm vi factual.
* Khuyến khích trao đổi với dược sĩ trong trường hợp đặc biệt.

---

## 7. Kế hoạch kiểm thử và bằng chứng demo

### Test Case 1 – Happy Path

**Input:**

> Paracetamol 500mg có tác dụng gì?

**Kỳ vọng:**

* Factual
* Trả lời ngay

---

### Test Case 2 – Advisory

**Input:**

> Tôi bị tiểu đường type 2 có dùng được Ibuprofen không?

**Kỳ vọng:**

* Route sang dược sĩ
* Không tự trả lời

---

### Test Case 3 – Low Confidence

**Input:**

> Thuốc này uống được không?

**Kỳ vọng:**

* Hỏi thêm thông tin

---

### Bằng chứng lưu trong repo

```text
evidence/
├── screenshots/
├── sample-questions.md
└── interview-notes.md

tests/
├── classifier-results.md
├── failure-path-results.md
└── screenshots/
```

---

## 8. Phân công

| Thành viên         | Trách nhiệm   | Deliverable                                                          |
| ------------------ | ------------- | -------------------------------------------------------------------- |
| Nguyễn Hoàng Dương | Research      | evidence/sample-questions.md                                         |
| Nguyễn Văn Phúc    | SPEC + Prompt | spec/spec.md, prompt-triage-classifier.md, prompt-handoff-summary.md |
| Vũ Đình Phượng     | Prototype     | src/                                                                 |
| Nguyễn Quang Hòa   | Testing       | tests/failure-path-results.md                                        |
| Tiền Anh Kiệt      | Demo + README | README.md, demo-script.md                                            |

---

## Phụ lục – Success Metrics

### User Metrics

* First response time < 5 giây.
* Tỷ lệ tiếp tục cuộc hội thoại > 80%.
* Giảm tỷ lệ bỏ chat.

### Business Metrics

* Giảm ít nhất 50% số câu hỏi factual chuyển đến dược sĩ.
* Giảm thời gian xử lý trung bình của dược sĩ.
* Tăng khả năng hỗ trợ ngoài giờ hành chính.

### AI Metrics

* Accuracy classifier ≥ 90%.
* Tỷ lệ route sai < 5%.

---

## Phụ lục – Keyword Trigger

Các trường hợp sau sẽ tự động route sang dược sĩ:

### Bệnh nền

* Tiểu đường
* Huyết áp
* Tim mạch
* Ung thư
* Suy gan
* Suy thận

### Đối tượng đặc biệt

* Trẻ sơ sinh
* Trẻ em dưới 2 tuổi
* Phụ nữ mang thai
* Phụ nữ cho con bú
* Người cao tuổi

### Tương tác thuốc

* Đang uống thuốc
* Đang điều trị
* Kết hợp thuốc
* Tương tác thuốc

### Triệu chứng nguy hiểm

* Khó thở
* Co giật
* Đau ngực
* Sốt cao kéo dài

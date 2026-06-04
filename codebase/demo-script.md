# Demo Script — Long Châu AI Triage (4–5 phút)

**Người trình bày:** Tiền Anh Kiệt (dẫn dắt) + cả nhóm phụ trách từng phần.
**Setup:** Prototype chạy sẵn tại `localhost:8501`. Tab dự phòng: screenshot từ `evidence/`.

---

## Phần 1 — Problem (45 giây)

> "Long Châu có tính năng chat tư vấn dược sĩ. Nhưng mọi câu hỏi — từ đơn giản đến phức tạp — đều vào cùng một hàng chờ. Chúng tôi tự test: hỏi 'Paracetamol tác dụng gì?' và chờ 4 phút. Kết quả: user bỏ kênh ra quầy."

*[Chỉ vào screenshot image_1.jpg hoặc image_2.jpg từ Day-5 evidence]*

> "Pain thật: câu đơn giản chiếm slot của dược sĩ như câu phức tạp — và dược sĩ phải hỏi lại context từ đầu mỗi lần."

---

## Phần 2 — Solution (30 giây)

> "Giải pháp: AI middleware ngồi trước hàng chờ. AI phân loại → factual thì tự trả lời ngay; advisory thì hỏi thêm context rồi tạo tóm tắt và route sang dược sĩ — với safety gate từ khoá chạy trước classifier, đảm bảo câu hỏi rủi ro luôn đến người thật."

*[Chỉ vào diagram trong slide hoặc vẽ nhanh trên board]*

> "Augment hay Automate? Conditional automation: AI tự làm trong scope hẹp, fail-safe về human khi bất định."

---

## Phần 3 — Demo (3 phút)

### Demo 1: Happy path — Factual (40 giây)
```
Input: "Paracetamol 500mg tác dụng gì?"
```
- Nhập câu hỏi → nhấn Enter.
- Chỉ ra: phản hồi trong <5 giây, có disclaimer cuối, model hiển thị là gpt-4o-mini.
- Nói: "Câu này AI tự trả lời. Dược sĩ không cần vào."

### Demo 2: Gather path (40 giây)
```
Input: "Thuốc đau đầu này uống được không?"
```
- Nhập → chờ phản hồi.
- Chỉ ra: AI hỏi lại thêm thông tin (không tự trả lời).
- Nhập thêm context: "Tôi bị dạ dày hay đau."
- Chỉ ra: Advisory gather → tiếp tục hội thoại.

### Demo 3: Failure path — Safety gate (50 giây)
```
Input: "Tôi đang điều trị tiểu đường type 2, có dùng Ibuprofen được không?"
```
- Nhập → chờ phản hồi.
- Chỉ ra: badge ⚠️, route = advisory_handoff, **không có AI answer**, handoff card có tên dược sĩ.
- Mở expander "Tóm tắt cho dược sĩ" → chỉ ra context đã được chuẩn bị sẵn.
- Nói: "Safety gate bắt từ khoá 'tiểu đường' trước khi LLM được gọi — đây là failure mode nguy hiểm nhất, và prototype xử lý đúng."

### Demo 4: Error path (20 giây)
- Tạm dừng backend (hoặc chuẩn bị sẵn screenshot).
- Chỉ ra: UI hiện "❌ Mất kết nối backend", không crash.
- Nói: "Error path demo được ngay trong UI."

---

## Phần 4 — Wrap-up (30 giây)

> "Stack: FastAPI + Streamlit + OpenRouter (gpt-4o-mini). Docker Compose — chạy bằng một lệnh. Mỗi thành viên có commit thực chất."

> "Câu hỏi dự kiến: 'Sao không automate hết?' → Câu advisory sai sót có hậu quả sức khoẻ thật, không thể hoàn tác. Dược sĩ vẫn là decider."

---

## Câu hỏi dự đoán & trả lời nhanh

| Câu hỏi | Trả lời |
|---|---|
| Classifier có chính xác không? | Test 15 câu: 13/15 đúng route. Safety gate cover 2 miss còn lại. |
| Sao không dùng fine-tuned model? | Prototype 1 ngày. gpt-4o-mini + prompt đủ chứng minh ý tưởng. |
| Dược sĩ thật có dùng được không? | Cần tích hợp vào queue system của Long Châu — ngoài scope prototype. |
| Chi phí? | ~$0.001–0.003/câu với 3 LLM calls. 1000 câu/ngày ≈ $1–3. |

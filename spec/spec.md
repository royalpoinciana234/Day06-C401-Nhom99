# SPEC — Long Châu AI Triage Middleware

> **Build slice:** Cho khách hàng Long Châu nhắn tin hỏi về thuốc, AI phân loại câu hỏi và hoặc trả lời ngay (factual) kèm disclaimer, hoặc thu thập context 1–2 câu rồi route sang dược sĩ kèm tóm tắt sẵn — với safety gate từ khóa luôn force-route câu hỏi rủi ro cao đến người thật.

---

## 1. Bằng chứng

| Evidence | Nguồn | Insight |
|---|---|---|
| Câu hỏi "Paracetamol tác dụng gì?" chờ 3–5 phút | Tự dùng chat Long Châu (ảnh chụp màn hình – image_1.jpg) | Câu factual đơn giản chiếm slot dược sĩ như câu phức tạp |
| User bỏ kênh chat ra quầy khi không có phản hồi nhanh | Phỏng vấn nhanh 2 người dùng | Nếu không phản hồi ngay, Long Châu mất cơ hội tư vấn |
| Câu tương tác thuốc chờ 8 phút nhưng dược sĩ trả lời tốt | Tự dùng chat Long Châu (ảnh chụp màn hình – image_2.jpg) | Câu phức tạp cần người thật — AI không thay; AI chỉ triage nhanh hơn + kèm context |
| Dược sĩ phải hỏi lại context từ đầu mỗi lần | Phỏng vấn nhanh | Gather context thủ công = tốn thời gian dược sĩ; AI gather trước → dược sĩ vào ngay |

**Giả định chưa có nguồn ngoài:** Tỷ lệ câu factual vs advisory trong hàng chờ thực tế — nhóm ước tính 60–70% câu là factual dựa trên self-use, chưa có dữ liệu log thật từ Long Châu.

---

## 2. Lát cắt để build

> Một khách hàng Long Châu gửi một câu hỏi về thuốc qua chat → AI phân loại → nếu factual: trả lời tức thì kèm disclaimer; nếu advisory: hỏi thêm 1–2 câu context rồi tạo handoff summary và route sang dược sĩ.

---

## 3. AI Product Canvas

| Ô | Nội dung |
|---|---|
| **Value** | Khách hàng Long Châu chờ 3–8 phút cho mọi câu hỏi, kể cả câu đơn giản. AI trả lời câu factual trong <3 giây và chuẩn bị context cho dược sĩ trước khi họ vào — giải quyết cả bottleneck thời gian chờ lẫn thời gian dược sĩ gather thông tin. |
| **Trust** | Mọi câu trả lời AI kèm disclaimer rõ. Advisory không bao giờ được AI trả lời. Keyword safety gate chạy trước classifier — nếu câu chứa từ rủi ro (bệnh mãn tính, đang uống thuốc), force-route ngay không qua AI. Dược sĩ là người quyết định cuối cùng cho mọi câu advisory. |
| **Feasibility** | Chi phí: ~$0.001/câu với gpt-4o-mini (3 LLM calls: classify + answer/gather + summary). Độ trễ: <5 giây round-trip. Rủi ro lớn nhất: classifier sai → mitigated bằng keyword gate + disclaimer. Ngưỡng dừng: nếu accuracy classify <80% trên test set thực tế, cần tighten prompts hoặc thêm keyword list. |
| **Tín hiệu học** | Khi dược sĩ chỉnh sửa handoff summary → delta là tín hiệu sai. Khi user click "Hỏi thêm dược sĩ" sau câu factual → tín hiệu factual bị classify đúng nhưng answer thiếu. Cả hai đi vào bộ test cases để tune prompt. Hiện tại: thu thập thủ công (prototype). |

---

## 4. Tăng năng lực hay tự động hóa

### Lựa chọn

**Conditional Automation (kết hợp Automation và Augmentation)**

### AI và con người tham gia như thế nào

| Thành phần | Vai trò                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------- |
| AI         | Phân loại câu hỏi, trả lời các câu hỏi factual, thu thập context và tạo handoff summary. |
| Dược sĩ    | Đánh giá và trả lời các câu hỏi advisory liên quan đến tình trạng sức khỏe cá nhân.      |
| Người dùng | Có thể yêu cầu chuyển sang dược sĩ bất kỳ lúc nào.                                       |

### Mức độ tự động hóa

Sản phẩm kết hợp cả hai cách tiếp cận:

#### Automation

AI tự hành động trong phạm vi đã định:

* Phân loại câu hỏi thành factual hoặc advisory.
* Trả lời các câu hỏi factual như công dụng, thành phần, cách bảo quản thuốc.
* Thu thập thông tin ban đầu từ người dùng.

#### Augmentation

AI hỗ trợ con người thay vì thay thế:

* Tóm tắt bối cảnh cuộc hội thoại.
* Chuẩn bị thông tin cho dược sĩ trước khi tư vấn.
* Giúp dược sĩ giảm thời gian hỏi lại thông tin đã có.

### Lý do lựa chọn

Nhóm chọn **Conditional Automation** vì không phải mọi câu hỏi đều có cùng mức độ rủi ro.

* Với các câu hỏi factual, AI có thể tự động xử lý an toàn và giúp người dùng nhận phản hồi gần như tức thì.
* Với các câu hỏi advisory như tương tác thuốc, liều dùng theo bệnh lý hoặc tư vấn cho đối tượng đặc biệt, AI chỉ đóng vai trò hỗ trợ thu thập và tổng hợp thông tin; quyết định cuối cùng vẫn thuộc về dược sĩ.

Long Châu đã có đội ngũ dược sĩ chuyên môn. Mục tiêu của sản phẩm không phải thay thế dược sĩ mà là phân luồng hiệu quả hơn, giảm tải các câu hỏi đơn giản và chuẩn bị sẵn context cho các trường hợp cần tư vấn chuyên sâu. Vì vậy, sản phẩm kết hợp **Automation ở các tác vụ rủi ro thấp** và **Augmentation ở các tác vụ cần chuyên môn con người**, trong một mô hình **Conditional Automation**.

---

## 5. Bốn đường đi của trải nghiệm

| Đường đi | Câu hỏi | Hệ thống xử lý |
|-----------|------------------------|----------------|
| **Đường thuận (Happy Path)** | *"Paracetamol 500mg có tác dụng gì?"* | AI phân loại là **Factual**, trả lời trực tiếp trong < 3 giây kèm disclaimer nhẹ. |
| **Khi AI không chắc (Low Confidence)** | *"Thuốc này uống được không?"* | AI không đủ thông tin để phân loại hoặc tư vấn an toàn. Hệ thống chuyển sang chế độ thu thập thêm ngữ cảnh và hỏi rõ hơn, ví dụ: *"Bạn đang hỏi về thuốc nào?"*, *"Bạn có đang dùng thuốc khác không?"*. |
| **Khi AI phát hiện rủi ro (Failure Path)** | *"Tôi bị tiểu đường type 2 có dùng được Ibuprofen không?"* | Keyword/rule gate phát hiện đây là câu hỏi **Advisory** có yếu tố bệnh lý. AI không tự trả lời, không đi qua luồng factual, mà tạo handoff summary và chuyển cho dược sĩ/chuyên gia. UI hiển thị trạng thái cảnh báo và handoff. |
| **Khi người dùng sửa (Correction Path)** | AI hiểu sai hoặc summary chưa chính xác. | Dược sĩ/chuyên gia chỉnh sửa summary và trả lời trực tiếp cho người dùng. Hệ thống lưu correction để cải thiện prompt, rule và test cases trong tương lai. |

---

## 6. Failure modes nguy hiểm nhất

**Lỗi 1 — Mis-classify advisory thành factual (nguy hiểm nhất)**
- Khi nào: câu tư vấn cá nhân không có từ khoá rõ ràng (ví dụ: "Vitamin C uống buổi sáng hay tối tốt hơn?" — có vẻ factual nhưng có thể có bệnh nền).
- Hậu quả: AI tự trả lời với thông tin chung → user tin dùng mà thiếu context bệnh nền → rủi ro sức khoẻ.
- Xử lý: (a) keyword safety gate force-route trước classifier; (b) disclaimer bắt buộc cuối mọi câu factual; (c) prompt classifier bias toward advisory khi lưỡng lự.

**Lỗi 2 — Classifier không nhất quán**
- Khi nào: cùng câu hỏi, model output thay đổi theo run.
- Hậu quả: trải nghiệm không đồng đều.
- Xử lý: JSON-mode strict, fallback to advisory nếu parse fail.

**Lỗi 3 — Handoff summary sai hoặc thiếu thông tin**
- Khi nào: context quá ngắn hoặc cuộc hội thoại ít turn.
- Hậu quả: dược sĩ phải hỏi lại từ đầu — mất giá trị của AI gather.
- Xử lý: prompt yêu cầu format cụ thể; prototype cho dược sĩ chỉnh summary trước khi tiếp nhận.

---

## 7. Kế hoạch kiểm thử và bằng chứng demo

**Test cases:** xem `codebase/sample-questions.md` — 15 câu hỏi labeled factual/advisory/force-route.

**Demo inputs chuẩn bị:**
- Happy: "Paracetamol 500mg tác dụng gì?" → factual, AI answer + disclaimer
- Gather: "Thuốc đau đầu này uống được không?" → advisory_gather, AI hỏi thêm
- Force-route: "Tôi đang điều trị tiểu đường, có dùng Ibuprofen được không?" → safety gate triggered, advisory_handoff

**Bằng chứng có sẵn:**
- Screenshot các case từ `codebase/triage-test-results.md`
- Tất cả LLM calls thật (OpenRouter, model gpt-4o-mini)

---

## 8. Phân công

| Thành viên | Mã HV | Phụ trách |
|---|---|---|
| Tiền Anh Kiệt | 2A202600961 | Scaffold repo, Docker Compose, demo script, README, UI polish |
| Vũ Đình Phượng | 2A202600634 | FastAPI backend, Streamlit frontend, Phase 2+3 integration |
| Nguyễn Văn Phúc | 2A202600539 | Prompts (classifier, answer, handoff), SPEC hoàn thiện |
| Nguyễn Hoàng Dương | 2A202600849 | Sample questions, evidence, test cases |
| Nguyễn Quang Hoà | 2A202600986 | Test failure paths, triage-test-results.md, dry run |
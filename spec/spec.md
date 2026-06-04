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

## 4. Augment hay Automate

**Chọn: Conditional Automation.**

AI tự hành động trong scope hẹp (factual) và fail-safe sang human khi bất định. Cụ thể:
- **Factual → AI tự trả lời** (automate): thành phần thuốc, công dụng chung, cách bảo quản — không có rủi ro cá nhân hoá.
- **Advisory → AI chỉ gather + tóm tắt, dược sĩ quyết định** (augment): tương tác thuốc, liều theo bệnh lý, tư vấn cá nhân — sai sót có hậu quả sức khoẻ thật, không thể hoàn tác.

**Tại sao mức này:** Dược sĩ Long Châu đang có sẵn — không cần thay. Cần triage tốt hơn và chuẩn bị context trước. Automate hoàn toàn advisory là không phù hợp với quy định dược và rủi ro pháp lý.

---

## 5. Bốn đường đi của trải nghiệm

| Đường đi | Input mẫu | Prototype xử lý |
|---|---|---|
| **Happy (factual)** | "Paracetamol 500mg tác dụng gì?" | AI classify factual → trả lời trong <3s kèm disclaimer nhẹ |
| **Low-confidence (gather)** | "Thuốc này uống được không?" | AI classify advisory + needs_context=true → hỏi "Bạn đang hỏi về thuốc nào? Bạn có bệnh nền hay đang dùng thuốc khác không?" |
| **Failure (force-route)** | "Tôi tiểu đường type 2, dùng Ibuprofen được không?" | Keyword gate bắt "tiểu đường" → force advisory_handoff, KHÔNG qua classifier, KHÔNG auto-answer; UI hiện badge ⚠️ + handoff card |
| **Correction** | Dược sĩ thấy summary sai | Dược sĩ sửa và trả lời trực tiếp; user thấy "Dược sĩ Lan đang hỗ trợ bạn" (mock trong prototype) |

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
| Tiền Anh Kiệt | HV001 | Scaffold repo, Docker Compose, demo script, README, UI polish |
| Vũ Đình Phượng | HV002 | FastAPI backend, Streamlit frontend, Phase 2+3 integration |
| Nguyễn Văn Phúc | HV003 | Prompts (classifier, answer, handoff), SPEC hoàn thiện |
| Nguyễn Hoàng Dương | HV004 | Sample questions, evidence, test cases |
| Nguyễn Quang Hoà | HV005 | Test failure paths, triage-test-results.md, dry run |

# Template — Evidence Pack

Nộp kèm thin SPEC cuối Day 05.

## 1. Nhóm và track

**Tên nhóm:** Nhóm X  
**Track:** Healthcare — Pharmacy / Medication Advisory  
**Product/app đã chọn:** Long Châu (app + website — có tính năng chat tư vấn với dược sĩ thật)  
**Build slice đang nghĩ:** Long Châu đã có chat dược sĩ thật. Thêm AI làm trung gian: khách nhắn tin → AI trả lời ngay câu hỏi factual (tác dụng thuốc, thành phần, cách dùng chung) → câu hỏi cần tư vấn cá nhân (chọn thuốc cho bệnh cụ thể, tương tác, liều đặc thù) thì AI tóm tắt context và route sang dược sĩ — dược sĩ không cần đọc lại từ đầu

## 2. Self-use evidence

Nhóm tự dùng app/workflow và ghi lại điểm gãy.

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Thử chat với dược sĩ Long Châu: hỏi "NANO FUCOIDAN tác dụng gì?" → chờ 3-5 phút mới có người trả lời | [Image 1](./image_1.jpg) - [Image 2](./image_2.jpg)  | Low-confidence, user phải chờ dù câu hỏi đơn giản | AI có thể trả lời ngay loại câu hỏi này; dược sĩ thật chỉ cần vào khi câu hỏi phức tạp |
| Hỏi "Tôi đang uống huyết áp, có dùng được Ibuprofen không?" → dược sĩ trả lời sau 8 phút, câu trả lời tốt | — | Người thật nhưng chờ lâu | Câu hỏi tương tác thuốc = cần người thật; nhưng AI nên route ngay thay vì để user chờ hàng |

## 3. User / review / social evidence

Nguồn có thể là review App Store/Play, group, comment, phỏng vấn nhanh, hoặc nguồn public khác.

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Hỏi thuốc cảm sốt cho bé 3 tuổi, nhắn tin xong ngồi chờ mãi không thấy dược sĩ online, cuối cùng tự ra quầy hỏi" | Phỏng vấn nhanh thành viên nhóm (người thân thật) | Phụ huynh mua thuốc cho con nhỏ, cần trả lời nhanh | Dược sĩ không available → user bypass hẳn kênh chat |
| "Bác sĩ kê 4 loại thuốc, mỗi loại uống khác giờ, mình đọc đơn mãi vẫn nhầm loại nào uống trước ăn loại nào sau ăn" | Gia đình thành viên nhóm | Bệnh nhân mãn tính 40-60 tuổi | Câu hỏi thật về thuốc, có thể AI trả lời được |
| "Nhắn tin hỏi thuốc nhưng dược sĩ hay hỏi lại nhiều câu trước khi trả lời, mất thời gian" | Phỏng vấn nhanh | Người mua thuốc OTC | Dược sĩ phải lấy thông tin thủ công mỗi lần → AI có thể làm bước này trước |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Intercom / Zendesk AI | AI trả lời câu hỏi thường gặp trước, route sang agent người khi không chắc; agent thấy full context khi nhảy vào | Pattern triage + handoff with context là chuẩn trong CS, áp được vào pharmacy chat | ✅ Pattern rõ, chỉ cần thay domain knowledge thành thuốc |
| Watsons HK (chat dược sĩ app) | Chat với dược sĩ thật, không có AI triage, mọi câu đều chờ người | Cùng pain với Long Châu, chờ lâu cho câu đơn giản | ✅ Xác nhận pain tồn tại ở cả competitor khu vực |
| Ada Health | AI hỏi triệu chứng từng bước → route sang bác sĩ khi cần; không tự chẩn đoán | Gather context bằng conversational flow, không hỏi 1 câu dài | ✅ Dùng pattern này cho bước gather context trước khi route dược sĩ |
| ChatGPT (workaround) | User tự hỏi ChatGPT về thuốc, được trả lời factual nhanh nhưng không có dược sĩ backup | Factual Q&A thuốc bằng LLM đã proven; thiếu là escalation path | ✅ Core prompt pattern cho phần AI trả lời factual |

## 5. Evidence → Insight

```text
Evidence nổi bật nhất:
- Long Châu đã có chat dược sĩ thật, nhưng user phải chờ 3-8 phút cho cả câu hỏi đơn giản lẫn phức tạp.
- Câu hỏi "Paracetamol tác dụng gì" và "Tôi đang uống huyết áp có dùng được Ibuprofen không"
  được xử lý cùng một queue → dược sĩ bị chiếm bởi câu hỏi dễ.
- Khi dược sĩ không online, user bypass hẳn kênh chat, mất lead.
- Dược sĩ phải gather context thủ công mỗi lần → tốn thời gian trước khi trả lời thật.

Insight:
User không chỉ cần "được trả lời".
Thật ra họ cần được trả lời NHANH, câu đơn giản trong vài giây, câu phức tạp cũng không chờ hàng,
vì hiện tại Long Châu không phân biệt loại câu hỏi, mọi thứ đều đi qua dược sĩ
nên dược sĩ quá tải với câu dễ, user chờ lâu cho câu khó.

Opportunity:
AI làm trung gian: tự trả lời câu hỏi factual ngay lập tức,
tự động gather context (thuốc đang dùng, triệu chứng) trước khi route,
rồi chuyển sang dược sĩ kèm tóm tắt, dược sĩ nhảy vào tư vấn ngay, không hỏi lại từ đầu.
```

## 6. Evidence đổi SPEC như thế nào?

- [ ] Đổi user chính.
- [x] Đổi pain statement — ban đầu nghĩ pain là "không có ai tư vấn", thực ra pain là "chờ lâu + dược sĩ bị chiếm bởi câu hỏi dễ".
- [x] Đổi build slice — đổi từ "thay dược sĩ bằng AI" sang "AI làm trung gian, dược sĩ vẫn là người quyết định cuối".
- [x] Đổi Auto/Aug decision — AI không thay dược sĩ; AI triage + route + gather context.
- [x] Đổi 4 paths — thêm path "AI route nhầm câu phức tạp ra trả lời luôn".
- [ ] Đổi owner/test plan.

Ghi rõ 1-2 thay đổi quan trọng:

```text
Trước evidence, nhóm định... dùng AI trả lời mọi câu hỏi thuốc thay dược sĩ.
Sau evidence, nhóm đổi thành... AI chỉ trả lời câu factual; câu cần tư vấn cá nhân thì AI gather context
  và route sang dược sĩ — vì Long Châu đã có dược sĩ thật, bỏ họ là giảm trust, không tăng.

Trước evidence, nhóm định... build từ đầu.
Sau evidence, nhóm đổi thành... build layer giữa: AI middleware cho chat sẵn có của Long Châu —
  scope nhỏ hơn, có thể demo trong 1 ngày.
```

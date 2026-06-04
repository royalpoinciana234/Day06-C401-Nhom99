# Template — Thin SPEC Cuối Day 05

Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.

## 1. Track, product/app và user

**Track:** Healthcare — Pharmacy / Medication Advisory  
**Product/app thật:** Long Châu — tính năng chat tư vấn dược sĩ (app + website)  
**User cụ thể:** Khách hàng Long Châu đang nhắn tin qua chat để hỏi về thuốc — có thể là thuốc đang mua, đang dùng, hoặc định mua cho người thân  
**Nhóm có phải user thật không? Nếu không, khác ở đâu?** Có — thành viên nhóm đã tự dùng chat Long Châu. Khác ở chỗ: nhóm ít lo lắng hơn khi chờ lâu; người dùng thật (đặc biệt phụ huynh hỏi thuốc cho con) có urgency cao hơn nhiều.

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Chat "Paracetamol tác dụng gì" → chờ 3-5 phút | Tự dùng Long Châu | Câu factual đơn giản chiếm slot dược sĩ như câu phức tạp | AI phải tự trả lời loại này, không route người |
| Người dùng bỏ qua kênh chat ra quầy khi dược sĩ không online | Phỏng vấn nhanh | Nếu không có phản hồi nhanh, user bỏ kênh — Long Châu mất tư vấn | AI phải available 24/7 cho câu factual |
| Câu tương tác thuốc chờ 8 phút nhưng dược sĩ trả lời tốt | Tự dùng Long Châu | Câu phức tạp cần người thật — nhưng chờ hàng quá lâu | AI không thay dược sĩ; AI route nhanh hơn + kèm context |
| Dược sĩ phải hỏi lại context từ đầu mỗi lần | Phỏng vấn nhanh | Gather context thủ công = tốn thời gian dược sĩ + bực bội user | AI gather trước khi route — dược sĩ vào tư vấn ngay |

## 3. Pain statement

```text
Khách hàng Long Châu hỏi về thuốc qua chat đang gặp khó ở bước chờ phản hồi,
vì toàn bộ câu hỏi — từ đơn giản đến phức tạp — đều vào cùng một hàng chờ dược sĩ thật,
dẫn tới chờ 3-8 phút cho mọi câu hỏi, và user bỏ kênh chat khi dược sĩ không online.
Bằng chứng chính là: self-use chat Long Châu (câu đơn giản chờ 3-5 phút) và phỏng vấn
user bypass ra quầy khi không có phản hồi nhanh.
```

## 4. Build slice

```text
Cho khách hàng Long Châu đang nhắn tin hỏi về thuốc,
prototype thêm AI làm trung gian trong luồng chat hiện có:
  AI nhận tin → phân loại (factual / advisory) →
    • Factual: AI trả lời ngay (tác dụng, thành phần, cách dùng chung)
    • Advisory: AI hỏi thêm 1-2 câu context (đang dùng thuốc gì, triệu chứng thế nào)
      rồi tạo tóm tắt và route sang dược sĩ thật
tạo ra: câu trả lời tức thì HOẶC handoff cho dược sĩ kèm tóm tắt context sẵn,
và xử lý failure "AI classify nhầm câu advisory thành factual" bằng cách
luôn thêm disclaimer "Nếu bạn đang điều trị bệnh cụ thể, hãy hỏi dược sĩ để được tư vấn chính xác hơn."
```

## 5. Auto/Aug decision

Chọn một:

- [ ] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [x] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:** Câu hỏi factual (tác dụng thuốc, thành phần) → AI trả lời an toàn. Câu hỏi cần tư vấn cá nhân (tương tác thuốc, liều cho bệnh cụ thể) → sai sót có hậu quả sức khoẻ thật → phải có dược sĩ thật quyết định. Long Châu đã có dược sĩ — không cần thay, chỉ cần triage tốt hơn.

**Human role:** dược sĩ là decider cho câu advisory; user là reviewer cho câu AI trả lời (có thể chọn "hỏi thêm dược sĩ").

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | User hỏi "Paracetamol 500mg tác dụng gì?" → AI classify factual → trả lời ngay trong <3 giây kèm disclaimer nhẹ |
| Low-confidence | User hỏi "Thuốc này có uống được không?" — thiếu thông tin — AI không đủ context để classify → hỏi thêm "Bạn đang hỏi về thuốc nào? Bạn có đang dùng thuốc khác không?" |
| Failure | User hỏi "Tôi tiểu đường type 2, có dùng được Ibuprofen không?" → AI nhận diện đây là advisory → KHÔNG tự trả lời → hỏi thêm 1 câu → route sang dược sĩ kèm tóm tắt "Khách tiểu đường type 2, hỏi về tương tác Ibuprofen" |
| Correction | Dược sĩ nhận handoff, thấy AI tóm tắt sai → dược sĩ sửa và trả lời trực tiếp; user thấy "Dược sĩ [tên] đang hỗ trợ bạn" |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user hỏi câu tư vấn cá nhân có rủi ro (ví dụ: tương tác thuốc khi đang điều trị bệnh mãn tính),
AI có thể classify nhầm thành factual và tự trả lời với thông tin chung — thiếu context bệnh nền của user,
hậu quả là user tin câu trả lời AI và dùng thuốc sai → nguy hiểm sức khoẻ thật.
Prototype sẽ xử lý bằng:
  1. Luôn thêm disclaimer cuối mỗi câu trả lời AI: "Nếu bạn đang điều trị bệnh cụ thể, hãy hỏi dược sĩ."
  2. Bất kỳ câu nào có từ khoá rủi ro (tên bệnh, "đang uống thuốc X", "bệnh mãn tính") → auto-route,
     không để AI classifier quyết.
```

## 8. Owner plan cho sáng Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| Nguyễn Hoàng Dương | Research: thu thập 10-15 câu hỏi thật từ Long Châu chat / App Store review để làm test cases cho classifier | `evidence/sample-questions.md` — factual vs advisory labeled |
| Nguyễn Văn Phúc | SPEC: hoàn thiện thin SPEC, viết prompt template cho classifier + response + handoff summary | `spec/prompt-triage-classifier.md`, `spec/prompt-handoff-summary.md` |
| Vũ Đình Phượng | Prototype: build chat UI đơn giản + gọi AI API với classifier prompt → 2 branch (trả lời / route) | `src/` — app chạy locally, demo happy path + failure path |
| Nguyễn Quang Hoà | Test / failure path: test 5 câu advisory, verify AI route đúng; test keyword trigger; document kết quả | `tests/triage-failure-path-results.md` — screenshot từng case |
| Tiền Anh Kiệt | Demo script + repo: kịch bản demo 4 phút (1 câu factual + 1 câu advisory + 1 failure), dọn repo, README | `README.md`, `demo-script.md` |

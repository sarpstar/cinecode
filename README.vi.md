<p align="center">
  <img src="docs/media/lockup.png" alt="cinecode" width="560">
</p>

<p align="center">
  <b>Những bộ phim được viết bằng code.</b><br>
  Phim ngắn, video YouTube dài, quảng cáo, video giải thích và video âm nhạc. Bạn mang đến ý tưởng và gu thẩm mỹ; một AI coding agent sẽ viết kịch bản, dựng mọi khung hình bằng code, thiết kế âm thanh và trao cho bạn một tệp MP4 hoàn chỉnh.
</p>

<p align="center">
  <a href="README.md">Türkçe</a> ·
  <a href="README.en.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="#cài-đặt">Cài đặt</a> ·
  <a href="#bắt-đầu-nhanh">Bắt đầu nhanh</a> ·
  <a href="#câu-hỏi-thường-gặp">Câu hỏi thường gặp</a>
</p>

<p align="center">
  <a href="https://github.com/sarpstar/cinecode/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/sarpstar/cinecode/tests.yml?branch=main&label=tests&style=flat-square" alt="tests"></a>
  <img src="https://img.shields.io/badge/license-MIT-C37232?style=flat-square" alt="license: MIT">
  <img src="https://img.shields.io/badge/agents-Claude%20Code%20%C2%B7%20Cursor%20%C2%B7%20Codex%20%C2%B7%20Antigravity-1a1a1a?style=flat-square" alt="agents: Claude Code, Cursor, Codex, Antigravity">
  <img src="https://img.shields.io/badge/render-three.js%20%C2%B7%20ffmpeg-1a1a1a?style=flat-square" alt="render: three.js, ffmpeg">
  <a href="https://x.com/sarpstar"><img src="https://img.shields.io/badge/X-%40sarpstar-1a1a1a?style=flat-square&logo=x&logoColor=white" alt="X: @sarpstar"></a>
</p>

<p align="center">
  <img src="docs/media/reel.gif" alt="30 giây từ những bộ phim làm bằng cinecode: vòm đá lúc bình minh, một đoàn tàu thư khắc linoleum trong tuyết, bộ máy đồng hồ chạm khắc, một chú thỏ 3D giữa sa mạc, thành phố thu nhỏ dưới cơn mưa code, cá voi pop-art dưới nước, con đường xuyên qua những cánh cổng màu cam, ba video giải thích dọc, máy quay phim trên đường ray giữa cánh đồng lúa mì, những chú chó dưới những cột ánh sáng vàng, một que diêm, một tiệm bánh và một tấm áp phích jazz, câu chuyện rừng với chiếc đèn lồng, một con tàu xa tít nơi chân trời trong đêm" width="100%">
</p>
<p align="center"><sub>30 giây từ những bộ phim làm bằng cinecode. Mọi khung hình đều được kết xuất từ code trong Chrome không giao diện.</sub></p>

Nó chạy trên chính máy tính của bạn: tốt nhất trong **Claude Code** (ứng dụng máy tính, tiện ích mở rộng VS Code, terminal), cũng chạy trong **Cursor**; người dùng đã chạy nó trong các agent khác như Codex và Antigravity nữa. Không cần dịch vụ trả phí nào; giọng đọc, chỉ khi bạn muốn có, dùng khóa Gemini của riêng bạn (có gói miễn phí), ElevenLabs, hoặc một giọng tiếng Thổ Nhĩ Kỳ miễn phí.

## Bạn có thể làm gì

### Phim ngắn, làm bằng code

Hãy nói điều bạn đang nghĩ trong một câu; phần còn lại bạn và agent cùng định hình.

- **Nó không chấp nhận điều hiển nhiên.** Agent kết hợp ý tưởng của bạn với một thứ có thật được rút ngẫu nhiên từ thế giới: một hiện vật bảo tàng, một con vật, một bức ảnh từ vũ trụ, một phát minh xưa, một di tích lịch sử, một nghề thủ công. Vì vậy thay vì bộ phim ai cũng sẽ làm đầu tiên, bạn nhận được những cách tiếp cận ý tưởng của mình mà chính bạn chưa từng nghĩ tới.
- **Nó không lặp lại chính mình.** Mọi gợi ý đều được kiểm tra với những bộ phim bạn đã làm, nên bạn không bao giờ nhận được cùng một bộ phim hai lần.
- **Bạn luôn là người quyết định cuối cùng.** Bạn chọn chất liệu làm phim: 3D với ánh sáng thật, hoạt hình 2D, sơn, mực, giấy, đất sét, motion graphics hay điểm ảnh. Bạn chọn diện mạo từ một bảng ảnh tĩnh trích từ các bộ phim thật, và bạn xem cùng duyệt hai cảnh đầu tiên trước khi toàn bộ bộ phim được dựng.

### Video dài cho YouTube

Phim tài liệu, video giải thích và tiểu luận video từ mười phút trở lên, được dựng ở chế độ Film theo các hồi và chương:

- một kịch bản có nghiên cứu, trong đó mọi khẳng định về một người hay sự kiện có thật đều mang theo nguồn của nó;
- một câu hỏi mở được gieo trong phút đầu tiên và một bản đồ tò mò giữ người xem đến cuối;
- một giọng đọc bằng ngôn ngữ của bạn (giọng tiếng Thổ Nhĩ Kỳ và tiếng Anh, kèm các giọng tiếng Thổ Nhĩ Kỳ miễn phí), với cách xử lý giọng riêng, không bao giờ là giọng thô của engine;
- ảnh lưu trữ, bản đồ, tài liệu và tư liệu từ các kho lưu trữ mở, và code ở nơi không có hình ảnh: bản đồ tự vẽ, bộ đếm, sơ đồ, địa điểm được dựng lại;
- thẻ chương khi hình thức cần đến, nhạc được chọn bằng tai cho từng hồi, bản master −14 LUFS và một tệp ghi công cho phần mô tả video của bạn.

### Phim quảng cáo và sản phẩm

Sản phẩm của bạn, màu sắc, phông chữ, logo và lời kêu gọi hành động của bạn. Sản phẩm được dựng chi tiết và chiếu sáng như một bức ảnh studio; phần mềm có các ảnh hero của giao diện; một bài kiểm tra tính đặc thù giữ cho bộ phim không thể vừa với bất kỳ thương hiệu nào khác; các phiên bản 9:16, 1:1 và 16:9 đi kèm vùng an toàn.

### Video giải thích cho mạng xã hội

Phim dọc từ 30 đến 60 giây: một câu hỏi ngay trong giây đầu tiên, chữ động từ một cặp phông mở đã kiểm tra cho tiếng Thổ Nhĩ Kỳ, sơ đồ dựng lên từng nét, chữ đọc được ở cỡ điện thoại.

### Video âm nhạc

Mang theo bài hát của bạn: lưới nhịp của nó được đo, các cắt dựng nằm trên các ô nhịp của nó và các điểm nhấn nằm trên các phách của nó, mỗi dòng lời là một hình ảnh.

### Và hơn nữa

- **Giống một video bạn yêu thích, nhưng khác đi:** hình thức của nó được đo (cắt dựng, nhịp độ, ánh sáng, màu sắc) và bộ phim được làm mới trên hình thức đó, không bao giờ từ khung hình của nó.
- **Một bản dựng từ tư liệu của chính bạn:** một video nói trước ống kính hay một bản ghi màn hình được cắt từ bản chép lời có mốc thời gian theo từng từ, các khoảng lặng được cắt bỏ, đồ họa khớp theo lời nói.
- **Một loạt phim trong một định dạng:** lưu định dạng của một bộ phim và làm tập tiếp theo trong định dạng đó.

Từ một clip 15 giây đến những bộ phim mười phút và hơn nữa. Quick mode làm một bộ phim dài tới khoảng 3 phút trong một phiên làm việc; Film mode đưa những bộ phim dài hơn qua các bước được duyệt. Phim càng dài, càng tốn nhiều thời gian và lượt sử dụng.

## Được làm bằng cinecode

<table>
  <tr>
    <td width="33%"><img src="docs/media/stills/motor.jpg" alt="Motor: một con sóng đông cứng khi vỡ, dưới bầu trời hoàng hôn"><br><sub><b>Motor</b> · những khoảnh khắc đông cứng · 90 s</sub></td>
    <td width="33%"><img src="docs/media/stills/tren.jpg" alt="The Mail Train: một toa thư đỏ trong khung cảnh tuyết khắc linoleum"><br><sub><b>The Mail Train</b> · một hành trình khắc linoleum · 25 s</sub></td>
    <td width="33%"><img src="docs/media/stills/ilktik.jpg" alt="İlk Tik: đường chân trời khắc trên bộ máy đồng hồ vàng"><br><sub><b>İlk Tik</b> · một quảng cáo đồng hồ · 50 s</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/stills/atlama.jpg" alt="Atlama Programı: thành phố giấy dưới cơn mưa code xanh lá"><br><sub><b>Atlama Programı</b> · một bản tri ân thu nhỏ · 50 s</sub></td>
    <td><img src="docs/media/stills/koltuk.jpg" alt="Boş Koltuk: máy quay phim trên đường ray giữa cánh đồng trống"><br><sub><b>Boş Koltuk</b> · một phim trường tự dựng nên · 80 s</sub></td>
    <td><img src="docs/media/stills/kopek.jpg" alt="Yüz Köpek: những chú chó thành điểm sáng dưới những cột sáng"><br><sub><b>Yüz Köpek</b> · một phim tài liệu dữ liệu · 90 s</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/stills/titanik.jpg" alt="Titanik, Son Saatler: con tàu đang chìm trên biển tối"><br><sub><b>Titanik, Son Saatler</b> · một phim tài liệu · 5 min</sub></td>
    <td><img src="docs/media/stills/cinecode.jpg" alt="cinecode: tháp cửa sổ nhiều màu kiểu pop-art"><br><sub><b>cinecode</b> · một video quảng bá pop-art · 60 s</sub></td>
    <td><img src="docs/media/stills/fener.jpg" alt="Fener: một cô bé và thần cây dưới ánh trăng"><br><sub><b>Fener</b> · một câu chuyện hoạt hình · 60 s</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/stills/gokyuzu.jpg" alt="Gökyüzü neden mavi?: lăng kính tách ánh sáng, với chữ vàng lớn"><br><sub><b>Gökyüzü neden mavi?</b> · một video giải thích · 45 s, 9:16</sub></td>
    <td><img src="docs/media/stills/firin.jpg" alt="Kuzguncuk Fırın: simit mới ra lò dưới ngọn đèn cạnh lò nướng"><br><sub><b>Kuzguncuk Fırın</b> · một quảng cáo tiệm bánh · 15 s, 9:16</sub></td>
    <td><img src="docs/media/stills/kibrit.jpg" alt="Tek Kibrit: thành phố khắc tỏa ánh đồng"><br><sub><b>Tek Kibrit</b> · một phim ngắn đồ họa · 63 s, 9:16</sub></td>
  </tr>
</table>

## Cách hoạt động

1. **Bạn nói ý tưởng.** Một câu là đủ; một bản brief đầy đủ sẽ đi thẳng vào việc.
2. **Nó hỏi vài câu hỏi** (các cách hiểu ý tưởng, phim được làm bằng gì, độ dài và định dạng, diện mạo, âm thanh và âm nhạc), mỗi câu đều có một đáp án gợi ý được đánh dấu ★.
3. **Nó trình bày kế hoạch** dưới dạng văn bản: các nhịp theo từng giây và một thẻ đạo diễn bạn có thể thay đổi từng dòng. Sau đó là hai cảnh dưới dạng ảnh tĩnh, trước khi phần còn lại được dựng.
4. **Nó kết xuất một bản nháp,** kiểm tra nó (chuyển động ngay từ khung hình đầu tiên, độ lớn âm thanh, khả năng đọc, sự lặp lại), cho bạn xem, và một người xem độc lập xem nó với con mắt mới. Ghi chú của bạn chỉ thay đổi những gì chúng chạm tới.
5. **Bản cuối:** kích thước đầy đủ, master ở −14 LUFS, kèm phần ghi công cho mô tả video của bạn.

## Hai chế độ

Agent hỏi điều này đầu tiên và gợi ý một chế độ cho mục tiêu của bạn.

| | **Quick mode** | **Film mode** |
|---|---|---|
| Một dòng | toàn bộ bộ phim trong một tệp, vài câu hỏi, một bản nháp độ phân giải thấp, 1–2 lần sửa | lộ trình và toàn bộ kịch bản được duyệt trước; sau đó sản xuất từng giai đoạn với sự đồng ý của bạn, hoặc đi thẳng tới bản nháp; nghiên cứu, âm thanh nhiều lớp |
| Hợp nhất cho | bất cứ thứ gì dưới khoảng một phút, kể cả sản phẩm thương hiệu và khách hàng; clip mạng xã hội, video giải thích, quảng cáo, các sản phẩm tới khoảng 3 phút; bản nháp đầu tiên của một phim ngắn trong vài phút, khoảng 3 lần duyệt | những bộ phim dài hơn với nhiều cảnh, tài liệu nghiên cứu hay lưu trữ: phim tài liệu, tác phẩm có giọng đọc, phim ngắn dự liên hoan; khoảng 6–8 lần duyệt theo từng giai đoạn, khoảng 3 lần nếu đi thẳng |
| Cách làm | vài câu hỏi (gồm chất liệu, giọng đọc, âm nhạc và tài liệu tham chiếu) → nghiên cứu tùy chọn (ảnh tĩnh từ những bộ phim giống của bạn, cộng hình dạng thật ở nơi chủ thể là thật) → kế hoạch dưới dạng văn bản (các nhịp, thẻ đạo diễn, bảng tham chiếu) → hai cảnh dưới dạng ảnh tĩnh chờ bạn duyệt, rồi phần còn lại → bản nháp độ phân giải thấp → tối đa 2 vòng sửa trên bản nháp → kết xuất cuối | 6 câu hỏi → lộ trình → kịch bản → khung phong cách → animatic → kết xuất; từng giai đoạn với sự đồng ý của bạn, hoặc từ kịch bản đi thẳng tới bản nháp |
| Hình ảnh | một `film.html` tự chứa: các cảnh là hàm của thời gian, Canvas 2D hoặc three.js / WebGL, chữ trên màn hình | các cảnh three.js với tám preset diện mạo, kết xuất theo từng cảnh quay |
| Âm thanh | được thiết kế từ phiên bản 1 trong cùng một tệp (Web Audio, kết xuất ngoại tuyến): một lớp âm thanh môi trường cho mỗi cảnh, hiệu ứng theo bảng tín hiệu của hình ảnh, một reverb chung, nhạc từ một bảng phối | một bản sắc âm thanh được thiết kế với các lớp nền, foley, khoảnh khắc điểm nhấn, giọng và nhạc |
| Các agent | một cuộc trò chuyện chính xây dựng, kết xuất và sửa (nhanh); nghiên cứu ở nền, các agent phụ chỉ cho bài kiểm tra dự đoán, kiểm tra trùng lặp, các bản thu giọng đọc và một người xem độc lập cho mỗi bản nháp | cuộc trò chuyện chính xây dựng những gì nó nắm; các agent phụ nhận những phần độc lập song song (âm thanh, giọng đọc, nghiên cứu, rà soát) và các chương của một bộ phim dài |

Bạn có thể bắt đầu ở Quick mode và chuyển một bộ phim sang Film mode sau: các nhịp trở thành lộ trình.

## Hai mục đích

Được hỏi cùng với chế độ: chế độ quyết định độ sâu của công việc, mục đích quyết định bộ phim thuộc loại nào. Mọi thứ sau đó (mặc định của các câu hỏi, tài liệu tham chiếu, các cổng, các kiểm tra) đều đi theo mục đích.

| | **Phim điện ảnh** | **Quảng cáo & sản phẩm** (thương hiệu, ra mắt, quảng bá, giải thích) |
|---|---|---|
| Mục tiêu | một câu chuyện, tâm trạng hay tác phẩm nghệ thuật trông như được quay, không phải được kết xuất | một bộ phim thuộc về một chủ thể, nói rõ nó là của ai và phải làm gì tiếp theo |
| Hình ảnh | lớp xử lý điện ảnh: tiêu cự nông và cá tính ống kính, hạt nhiễu, quán tính của người quay, và theo yêu cầu (mặc định tắt) nhòe chuyển động 180° ở các chuyển động nhanh, sắc thái phim từ đường cong in của chính bộ công cụ và độ rung cổng phim; chuyển động máy được chọn cho từng cảnh quay | bài kiểm tra tính đặc thù và đối thủ, tên trên màn hình dưới dạng lower third, ảnh hero giao diện cho phần mềm, màu và phông thương hiệu của bạn (phông mở từ Fontsource; phông thương hiệu riêng của bạn ở lại máy bạn), một thẻ kết thúc với lời kêu gọi hành động |
| Âm thanh | dẫn dắt bằng âm thanh môi trường, một âm thanh đặc trưng, bản nhạc bạn chọn | giọng đọc + nhạc theo mặc định |
| Bàn giao | định dạng bạn chọn | các biến thể 9:16, 1:1 và 16:9 với vùng an toàn |
| Thêm | — | tùy chọn: tư liệu của chính bạn hay bản ghi màn hình được cắt từ bản chép lời có mốc thời gian theo từng từ (cần Whisper): cắt khoảng lặng, cờ đánh dấu đoạn vấp và quay lại chờ bạn duyệt, đồ họa khớp theo lời nói |

Chi tiết: `references/purpose-cinematic.md`, `references/purpose-ad.md`, `references/footage-edit.md`. Chuyển động, từ vựng máy quay, phông chữ, đồng bộ âm thanh, điểm hook, một hành động cho mỗi cảnh quay và các kiểm tra được cả hai dùng chung.

## Bạn nhận được gì

- **Một hệ thống viết** cho những kịch bản thông minh, ngắn gọn, đúng đích (cả hai chế độ): phân kỳ rồi hội tụ, một bước ngoặt rõ ràng khi câu chuyện có một bước ngoặt, viết kết thúc trước, cho thấy thay vì kể, một ngân sách từ ngữ, một danh sách cấm sáo ngữ bằng tiếng Anh và tiếng Thổ Nhĩ Kỳ, một lượt đọc thành tiếng và cắt 30%, một bài kiểm tra người xem lần đầu.
- **Một từ vựng máy quay và chuyển cảnh có tên** (`references/camera-moves.md`): các chuyển động, chuyển tiêu điểm và chuyển cảnh (dolly in, orbit, dolly zoom, FPV, handheld, speed ramp, rack focus, match cut, whip pan, J-cut…) kèm cảm giác mỗi thứ mang lại cho người xem, thời lượng, tốc độ và easing mặc định. Máy quay của mỗi cảnh quay là một dòng: *"dolly in, 3 s, slow ease-in-out, toward the figure"*. Cả hai engine đều cài đặt chúng dưới dạng hàm thuần của thời gian (`film.html` máy quay 2.5D, `starter/camera.mjs` cho three.js).
- **Bộ khởi đầu Quick mode:** `film.html` với một dòng thời gian xác định, máy quay 2.5D với các mặt phẳng chiều sâu, chuyển cảnh, một bảng tín hiệu chung cho hình và tiếng, tính ngẫu nhiên có hạt giống (với bộ nhớ đệm lười cho dữ liệu có hạt giống), các trợ giúp chữ và nhãn tên được định cỡ cho dấu phụ, và các giọng Web Audio nhỏ (pad, kick, tick, hit, riser, whoosh, pluck, một lead mềm, foley, các lớp âm thanh môi trường, một reverb tạo chung) với một bảng phối được kiểm tra trước mỗi lần kết xuất. Nhấp vào nó trong trình duyệt sẽ phát hình và tiếng cùng nhau.
- **Buổi phỏng vấn của Film mode** gồm sáu câu hỏi trong ba vòng ngắn (bảng định hướng được trình bày giữa các vòng), và **tám preset diện mạo** (điện ảnh thực tế, anime/cel, truyện tranh pastel, claymation, cắt giấy/collage, retro/synthwave/VHS, quảng cáo bóng bẩy, mực vẽ tay), cộng một đường tới diện mạo tùy chỉnh từ hình ảnh tham chiếu của chính bạn. Tám họ diện mạo đó cũng hoạt động trong Quick mode (chỉnh màu, kết cấu, tô bóng toon, vẽ theo từng hai khung).
- **Một giọng thuộc về bộ phim:** giọng đọc không bao giờ ra ngoài dưới dạng giọng thô của engine. Mỗi bộ phim chọn cách giọng của nó đi qua (gần, băng, radio, hợp xướng, dưới nước, máy móc…), nơi nó đứng (một căn phòng, một sảnh, một gian nhà đá, ngoài trời) và có thể mang âm thanh đặc trưng của bộ phim bên trong nó; mọi câu thoại đều đáp ở cùng một mức âm lượng hội thoại.
- **Giống video này, nhưng …:** thả một video bạn thích vào `refs/` và nói điều muốn thay đổi. Hình thức của nó được đo (cắt dựng và độ dài cảnh quay, nhịp độ, bảng màu và ánh sáng, BPM, cách các cắt dựng nằm trên nhịp), bạn thay đổi điều mình muốn, và bộ phim được làm mới trên hình thức đó, không bao giờ từ khung hình hay nhạc của nó.
- **Bài hát của chính bạn:** mang theo một bài hát hay một track và bộ phim đi theo lưới nhịp của nó: nhịp độ được đo trên toàn bộ bài hát, clip được cắt trên một vạch ô nhịp, các cắt dựng và điểm nhấn nằm trên ô nhịp và phách, mỗi dòng lời là một hình ảnh; nhạc tự nhỏ xuống dưới giọng đọc.
- **Bảng định hướng (Film mode):** khi bạn nói ý tưởng của mình, ba định hướng hình ảnh được trình bày trong một hình, mỗi định hướng là một phong cách cộng ảnh tĩnh từ hai hay ba bộ phim thật mà diện mạo của chúng mang nó (FilmGrab, chỉ để lấy tâm trạng) với bảng màu đã đo của nó; định hướng bạn chọn được đo vào ánh sáng và màu sắc của bộ phim, và khung phong cách được kiểm tra với nó.
- **Diện mạo được tìm cho từng ý tưởng:** các định hướng từ điện ảnh thật (ảnh tĩnh từ phim, nhà quay phim và nhiếp ảnh gia, chỉ để lấy tâm trạng) và một kệ công thức phong cách làm từ vựng (khắc gỗ, ukiyo-e, rối bóng, risograph, phim câm và hơn nữa; phần lớn trong số chúng của LemoLab, xem phần Ghi công); chỉ định hướng được chọn mới được đọc.
- **Typography đẳng cấp thiết kế** (`references/typography.md`): các phông và cặp phông sạch về giấy phép, đã kiểm tra cho tiếng Thổ Nhĩ Kỳ, từ các xưởng phông mở độc lập và Fontsource; ba cặp phông được chia cho mỗi bộ phim và trình bày dưới dạng thẻ mẫu trong chính diện mạo của bộ phim; tài liệu tham chiếu typography từ Fonts In Use, Art of the Title, Typewolf, Are.na và ảnh chụp màn hình của chính bạn (kể cả các lưu Instagram) trong `refs/type/`, được đo thành một định hướng chữ; một nhật ký gu học theo lựa chọn của bạn qua các bộ phim; kiểm tra khả năng đọc ở cỡ điện thoại, độ tương phản và dấu phụ; phụ đề khóa theo từ cho video người nói trước ống kính, tùy chọn.
- **Thiết yếu của thiết kế âm thanh:** một bản sắc âm thanh nhẹ cho mỗi bộ phim, các lớp nền, công thức ffmpeg đã kiểm thử, một bản master −14 LUFS.
- **Các công cụ nhỏ, không phụ thuộc:** chụp khung hình (cũng xuất thẳng ra MP4, và nhạc nền của trang ra WAV), dựng animatic, trộn âm, master, kiểm tra chất lượng (gồm một bài kiểm tra hook được đo, hành động của chủ thể trong mỗi cảnh sau khi loại bỏ chuyển động máy, và độ lớn cùng độ chói theo từng cảnh), tìm tài sản giấy phép mở với một nhật ký giấy phép.

## Yêu cầu

- Một AI coding agent có thể chạy các công cụ cục bộ: **Claude Code** (ứng dụng máy tính, tiện ích mở rộng VS Code hoặc terminal); **Cursor** hoặc một agent khác có thể chạy công cụ (Codex, Antigravity…) cũng được. Cuộc trò chuyện thông thường tại claude.ai không thể chạy công cụ trên máy tính của bạn; Claude Code thì có (ffmpeg, Chrome, các script).
- Node.js 22+, Python 3.9+, ffmpeg và Google Chrome (hoặc Chromium / Edge); agent cài đặt những gì còn thiếu, với sự đồng ý của bạn. Không gì khác, kể cả trên Windows: bộ công cụ chạy trong chính PowerShell của Claude Code, không có bash; Git chỉ được dùng để cài đặt và cập nhật bộ công cụ, không bao giờ để kết xuất. Nếu cơ chế bảo vệ của bộ công cụ không chạy trong một phiên Claude Code, phần thiết lập của bộ phim sẽ nói GUARD OFF (các kiểm thử chạy trên Windows và Linux ở mỗi lần push, và trên macOS trước mỗi thay đổi; một bộ phim trọn vẹn làm trên Windows thì chưa được thử). Các hook cần một Claude Code gần đây (hook dạng exec và `onFailure`, 2.1.295 hoặc mới hơn); trên một client cũ hơn, cơ chế bảo vệ có thể không đăng ký được và bộ phim vẫn chạy.
- Một GPU mà Chrome có thể dùng (bất kỳ máy Mac gần đây nào, hoặc một PC với driver đồ họa hoạt động).
- Dung lượng đĩa: Quick mode dẫn khung hình thẳng vào MP4, nên vài trăm MB là đủ; Film mode cần vài GB cho mỗi bộ phim trong lúc kết xuất.

Thiếu một trong số đó? Cứ bắt đầu: agent kiểm tra máy trước và đề nghị cài đặt những gì còn thiếu (nó hỏi trước khi cài bất cứ thứ gì). Không có gì khác được cài: các script chỉ dùng thư viện tích hợp sẵn, và three.js tải các phiên bản thư viện đã ghim từ một CDN.

**Các giọng tiếng Thổ Nhĩ Kỳ miễn phí, nếu bạn muốn một giọng** (bộ công cụ không cài giọng nào trong số chúng; giọng đọc nếu không sẽ dùng Gemini TTS với khóa của bạn, hoặc giọng hệ thống làm phương án tạm):
- [EMA Lightning](https://huggingface.co/canberkkkkkk/ema-lightning) của Canberk Aslan (Apache 2.0): một giọng rõ ràng, ngoại tuyến trên CPU, khoảng 800 MB với PyTorch. Bộ công cụ có thể dùng nó sau khi cài: `python3 tools/tts.py --install ema`, rồi `--engine ema`.
- [VoxCPM2 Türkçe ses tasarımı](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi) (Apache 2.0): thiết kế một giọng từ một mô tả, bảy giọng đọc sẵn (một giọng tài liệu, một người kể chuyện trầm, một phát thanh viên tin tức); Apple Silicon hoặc card NVIDIA, khoảng 3.7 GB.
- [Ahenk](https://github.com/ozguradmin/ahenk-turkish-tts) của Özgür Güler: ngữ điệu câu hỏi, cảm xúc và tiếng cười (mô hình lớn, card NVIDIA) và Ahenk Cep (nhỏ, CPU); các trọng số là CC BY 4.0, nên một bộ phim dùng chúng phải ghi công Ahenk.

## Cài đặt

Mở Claude Code (tab **Code** của ứng dụng máy tính, tiện ích mở rộng VS Code hoặc terminal) và nói:

> Install the cinecode skill from https://github.com/sarpstar/cinecode

Nó lấy bộ công cụ từ GitHub bằng git vào `~/.claude/skills/cinecode` (Windows: `%USERPROFILE%\.claude\skills\cinecode`); trên một máy Windows không có git, nó cài git trước (`winget install --id Git.Git -e`), sau khi bạn đồng ý. Sau đó mở một cuộc trò chuyện mới. Về sau, **"update cinecode"** mang đến phiên bản mới nhất. Chỉ cài nó ở một nơi duy nhất, để agent không thấy hai bản sao.

Bằng tay, tương tự trong một dòng:

```bash
git clone https://github.com/sarpstar/cinecode.git ~/.claude/skills/cinecode
```

Skill khởi động trên các cụm từ phim, hoạt hình và quảng cáo hằng ngày ("kısa film", "animasyon", "reklam filmi", "ürün videosu", "tanıtım videosu", "make a short film", "product video", "ad").

### 1. Ứng dụng Claude trên máy tính (Code)

Mở ứng dụng Claude trên máy tính, chuyển sang **Code**, chọn một thư mục trống cho bộ phim của bạn, và gõ **"I want to make a short film"** (tiếng Thổ Nhĩ Kỳ: **"Kısa film yapmak istiyorum"**).

### 2. Tiện ích mở rộng VS Code (Claude Code)

Cài tiện ích mở rộng Claude Code, mở một thư mục trống, mở bảng Claude Code và gõ cùng câu đó.

### 3. Terminal

```bash
mkdir my-film && cd my-film && claude
```

Sau đó gõ cùng câu đó.

### 4. Cursor

Trong cuộc trò chuyện Agent của Cursor, yêu cầu cài đặt tương tự vào `~/.cursor/skills/cinecode`, hoặc:

```bash
git clone https://github.com/sarpstar/cinecode.git ~/.cursor/skills/cinecode
```

Mở một thư mục trống trong Cursor, mở cuộc trò chuyện Agent và gõ cùng câu đó. Các kiểm tra của chính bộ công cụ (`make.py`, `qc.py`) chạy như nhau; các hook bảo vệ ngăn một vài sai lầm ngay khi chúng xảy ra (một script bị hỏi tới trước khi nó được trình bày, một bản nháp không được trình bày, một điểm dừng ngay sau một lần duyệt) chỉ chạy trong Claude Code.

### 5. Các agent khác (Codex, Antigravity…)

Nếu bạn dùng một agent khác có thể chạy công cụ và đọc skill, hãy bảo nó:

> Install the cinecode skill from https://github.com/sarpstar/cinecode into your skills folder

Agent biết thư mục của chính nó. Các công cụ và kiểm tra của bộ công cụ cũng chạy ở đó; các hook bảo vệ chỉ chạy trong Claude Code. Người dùng đã chạy nó trong các agent này; Claude Code là thiết lập được khuyến nghị.

## Bắt đầu nhanh

1. Mở một thư mục trống trong agent của bạn (xem phần Cài đặt).
2. Viết ý tưởng của bạn. Ý tưởng là thứ duy nhất bạn cần; bỏ qua phần còn lại nếu bạn chưa chắc, và agent sẽ hỏi:

   ```text
   Let's make a film with cinecode: <what it is about, a sentence or two>.

   (Add these if you know them; leave them out and the kit asks:)
   Length: <15 s / 1 min / 5 min…>
   Where it will be shown: <Instagram vertical / YouTube horizontal…>
   Sound: <a narrator / no voice / my own song: file>
   Look: <a film, a photo or a painter you have in mind, or "suggest one">
   ```

   Bỏ qua chế độ: agent gợi ý một chế độ từ quy mô công việc. Bạn càng viết ít, nó càng hỏi nhiều; một bản brief đầy đủ (các nhịp, lời, độ dài, định dạng) đi thẳng tới bản nháp mà không cần câu hỏi.
3. Chọn một chế độ và một mục đích (phim điện ảnh, hoặc quảng cáo & sản phẩm), trả lời các câu hỏi trong một hay hai vòng ngắn (lựa chọn được gợi ý được đánh dấu ★).
4. Duyệt hoặc thay đổi tại mỗi điểm kiểm tra. Bộ phim hoàn chỉnh đáp xuống đầu thư mục của bộ phim dưới tên `<title>.mp4`.

## Quick mode, từng bước

| # | Bước | Bạn làm |
|---|---|---|
| 1 | **Vài câu hỏi:** ý tưởng của bạn, chất liệu (phim được làm bằng gì), độ dài và định dạng, phong cách và tâm trạng, âm thanh (giọng đọc + nhạc, chỉ nhạc và hiệu ứng, hoặc chữ trên màn hình + nhạc; với giọng đọc còn có loại giọng và ngôn ngữ), âm nhạc riêng của nó (một bản thu thật bạn chọn bằng tai, track của chính bạn, viết bằng code, hoặc không có), tài liệu tham chiếu (tìm kiếm, chỉ của bạn, hoặc bỏ qua); bản sắc âm thanh được gợi ý trong một dòng | trả lời, hoặc "ok" |
| 1b | **Nghiên cứu nhẹ, nếu bạn đã chọn:** tài liệu tham chiếu giấy phép mở cho các yếu tố chính của chủ thể, nhiều hơn khi bộ phim dài hơn (2–3 cho 15–30 s, 3–5 cho 60 s, 2 cho mỗi chương trở đi; cộng `refs/` của bạn) | — |
| 2 | **Kế hoạch (một cổng văn bản):** logline, bước ngoặt, một bảng nhịp theo từng giây với các dòng máy quay (một dòng chảy, nhóm theo chương nội bộ cho các bộ phim dài hơn), chữ hoặc lời thoại; bảng tham chiếu khi đã chạy nghiên cứu; một thẻ đạo diễn ngắn (diện mạo, máy quay, chuyển động, nhịp độ, chuyển cảnh, chữ, âm thanh, hoàn thiện) bạn có thể thay đổi từng dòng | OK, đổi một tài liệu tham chiếu, một ghi chú, hoặc yêu cầu thêm tài liệu tham chiếu |
| 3 | **Hai cảnh trước:** diện mạo và hai cảnh (cảnh mở đầu và cảnh ít giống nó nhất) dưới dạng ảnh tĩnh, trước khi phần còn lại được dựng | tiếp tục, hoặc một ghi chú |
| 4 | **Dựng và bản nháp:** một `film.html` với hình và tiếng, một bản nháp nửa kích thước không có hiệu ứng hoàn thiện, master ở −14 LUFS, hook đã kiểm tra | xem, rồi OK hoặc ghi chú |
| 5 | **Sửa trên bản nháp:** tối đa hai vòng chỉnh sửa có mục tiêu, mỗi vòng được trình bày dưới dạng một bản nháp mới | gửi ghi chú trong một lượt |
| 6 | **Kết xuất cuối:** kích thước đầy đủ, với các hiệu ứng hoàn thiện bạn đã bật (nhòe chuyển động, sắc thái in, độ rung cổng phim; tất cả mặc định tắt), kiểm tra lại | xem |

## Film mode, sáu bước

| # | Bước | Bạn làm |
|---|---|---|
| 1 | **Phỏng vấn:** sáu câu hỏi trong ba vòng ngắn, bảng định hướng ở giữa các vòng | trả lời, hoặc chọn các lựa chọn ★ |
| 2 | **Lộ trình:** ý tưởng, các cảnh quay với thời lượng (bao nhiêu tùy độ dài cần: 4–8 cho 30 s, nhóm thành chương và hồi cho các bộ phim dài hơn), diện mạo, bản sắc âm thanh, hook, rủi ro | duyệt hoặc thay đổi các dòng |
| 3 | **Kịch bản và văn bản:** góc nhìn, bước ngoặt, lời thoại (hoặc không lời), chữ trên màn hình; toàn bộ kịch bản được trình bày cùng lúc | duyệt hoặc thay đổi; chọn cách sản xuất chạy: từng giai đoạn, hoặc tất cả đi thẳng tới bản nháp |
| 4 | **Khung phong cách:** một ảnh tĩnh ở chất lượng cuối, thước đo cho mọi khung hình về sau | duyệt hoặc cho một ghi chú |
| 5 | **Animatic:** một video độ phân giải thấp có mốc thời gian với âm thanh tạm | nhịp độ đã đúng chưa? |
| 6 | **Kết xuất, âm thanh, bản cuối:** một bản nháp nửa kích thước được cắt với âm thanh đã trộn trước, rồi hình ảnh kích thước đầy đủ, master, kiểm tra, bàn giao | xem, gửi ghi chú trong một lượt |

Các ghi chú chỉ được áp dụng cho các cảnh quay, lời thoại hay lớp âm thanh mà chúng chạm tới; mỗi vòng là một phiên bản mới. Sau khi bạn duyệt bản cuối, agent hỏi có nên dọn các bản nháp và tệp trung gian không; bộ phim đã bàn giao, tài liệu tham chiếu, tài sản, nguồn âm thanh và ghi chú của bạn luôn ở lại.

**Các quy tắc tích hợp (cả hai chế độ):** 2 giây đầu tiên chuyển động ngay từ khung hình 1 (được đo); mọi khung hình là một hàm thuần của thời gian (kết xuất lại cho kết quả giống hệt); mọi tệp bên ngoài đều có một dòng giấy phép khi nó được tải xuống; các kết xuất dài chạy ở nền với một tệp trạng thái; agent nhìn các bảng tiếp xúc nhỏ thay vì khung hình kích thước đầy đủ, điều này giữ chi phí thấp.

**Ai làm việc (Film mode):** cuộc trò chuyện chính xây dựng những gì nó đã nắm ngữ cảnh; một agent phụ mới, được giao brief từ các tệp dự án với mô hình của nó được nêu tên, nhận một phần độc lập chạy song song (âm thanh, các bản thu giọng đọc, nghiên cứu, người xem độc lập) hoặc một chương của một bộ phim dài; ghi chú của bạn được lưu nguyên văn trong `notes/round-N.md` và chỉ những cảnh quay chúng chạm tới mới được làm lại; một lỗi được chẩn đoán trên vài khung hình kiểm tra trước khi bất cứ thứ gì được dựng lại. Tại các điểm kiểm tra, agent có thể đề nghị một cuộc trò chuyện mới: trong ứng dụng Claude trên máy tính, nó tự mở sau khi bạn đồng ý; ở nơi khác, bạn mở một cuộc và dán một dòng duy nhất, **"Continue from STATE.md"** (tiếng Thổ Nhĩ Kỳ: **"STATE.md'den devam et"**). Chi tiết: `references/context-protocol.md`. Mỗi bước của một cuộc trò chuyện đều đọc lại toàn bộ cuộc trò chuyện, nên một cuộc trò chuyện ngắn là điều giữ một bộ phim rẻ: mỗi agent phụ bắt đầu trên mô hình mà nhiệm vụ của nó cần (gu và phán đoán trên mô hình của cuộc trò chuyện của bạn, công việc tệp và tìm nguồn trên các mô hình nhẹ hơn), các kết xuất trả lời trong bốn dòng (`tools/make.py`), và hình ảnh giữ ở kích thước nhỏ. Trong Claude Code, skill thực thi điều này bằng ba hook khởi động cơ chế bảo vệ của bộ công cụ; trong số các kiểm tra của nó: một nhắc nhở khi cuộc trò chuyện lớn dần, không hình ảnh lớn trong cuộc trò chuyện, giới hạn 25 bước cho mỗi agent phụ, không hỏi về điều gì người dùng chưa thấy, tệp khóa được giữ đóng.

## Bên trong có gì

```text
cinecode/
├── SKILL.md              the skill: the flow, the questions and the hard rules; every film chat starts here
├── AGENTS.md             the entry point for agents that read AGENTS.md
├── references/           the craft guides
│   ├── quick-mode.md     Quick mode, step by step
│   ├── film-mode.md      Film mode: six approved steps
│   ├── writing.md        script, hook, prediction test, overlap check
│   ├── looks.md          look, light, texture; with craft.md and finish.md
│   ├── camera-moves.md   camera language; motion with motion.md and motion-design.md
│   ├── typography.md     type; sound.md for sound, music-video.md for your own song
│   └── purpose-*.md      cinematic film, or ad and product
├── scripts/              the tools (Python standard library and Node)
│   ├── init_film.py      sets up the film's folder
│   ├── make.py           stills, draft and final, one command each
│   ├── capture.mjs       frame-by-frame render in headless Chrome
│   ├── deal.py, dice.py  sparks and the outside dice
│   ├── direction.py      the style board; with styles.py, asset_search.py, fonts.py
│   ├── mix.py            the mix; master_audio.py (−14 LUFS), tts.py (narrator), beat_grid.py
│   ├── qc.py             quality checks; with scene_check.py, words_check.py
│   └── guard.py          the guard: enforces the rules on the spot (with hook.cjs, Claude Code)
├── templates/            a new film's files and the Quick mode starter page
├── starter/              the three.js scene: eight looks, named camera moves, a type layer
├── styles/               58 style recipes (51 from lemo-opuscar, MIT; 7 the kit's own)
├── docs/                 README images and the font library
└── tests/                the test suite, run on Windows and Linux on every push
```

Một thư mục phim mà bộ công cụ thiết lập:

```text
my-film/
├── <title>.mp4           the finished film
├── STATE.md              where the film stands; every new chat continues from here
├── film.html             Quick mode: the film itself, one page of code
├── ROADMAP.md, SCRIPT.md Film mode: roadmap and script; the scenes live in engine/
├── refs/, research/      your references and the research
├── audio/, assets/       sound and downloaded material; their licences in LICENSES.csv
├── review/, renders/     check frames and drafts
└── tools/                this film's copy of the kit's tools
```

**Mọi thứ được lưu ở đâu:** mỗi bộ phim là thư mục của riêng nó (bộ phim hoàn chỉnh nằm ở đầu của nó dưới tên `<title>.mp4`). Những gì mang qua từ phim này sang phim khác sống trong `~/.cinecode/`: các khóa API của bạn (`keys.env`, nhập một lần), các định dạng đã lưu, nhật ký gu và bộ nhớ đệm tải xuống. Thư mục của chính bộ công cụ không bao giờ bị ghi vào.

## Câu hỏi thường gặp

**Chỉ code, hay lai?** Code là cốt lõi: hình ảnh được làm bằng code, không tốn chi phí mô hình. Bộ phim càng dài và càng nhiều tính thực tế, càng có nhiều tư liệu thật tham gia ở nơi code không thể hiện được sự vật thật: tư liệu và ảnh mà agent tự tìm trong các kho lưu trữ mở (Wikimedia Commons, Internet Archive, NASA, các bảo tàng) và ảnh cùng video stock từ Pixabay (khóa miễn phí của bạn, hỏi một lần), mỗi thứ đều được ghi lại với giấy phép của nó và được ghi công. Về âm thanh, bộ công cụ gợi ý một bản nhạc thu sẵn và các hiệu ứng âm thanh làm sẵn (các thư viện CC0 miễn phí); âm thanh tổng hợp hoàn toàn là một lựa chọn bạn có thể đưa ra. Bạn có thể thêm tư liệu, ảnh và bản ghi của chính mình. Nếu bạn tự kết nối một trình tạo hình ảnh hay video (Higgsfield, fal hoặc một cái khác), agent chỉ dùng nó khi bạn yêu cầu, như phương án cuối cùng; nó không bao giờ gợi ý một cái. Khuôn mặt hoạt động tốt nhất khi được cách điệu hoặc dưới dạng bóng ở các cảnh cận.

**Tôi có phải nhập khóa API cho mỗi bộ phim không?** Không. Lần đầu tiên giọng đọc cần một khóa, bạn nhập một lần duy nhất: agent mở tệp khóa trong trình soạn thảo văn bản của bạn với một dòng `GEMINI_API_KEY=` để trống; khóa không bao giờ đi vào một cuộc trò chuyện, một thư mục phim hay một repository.

**Làm sao tôi biết nó có thể làm gì?** Hãy hỏi: "what can you make?" ("neler yapabilirsin?"). Bạn nhận được một menu ngắn: một phim ngắn, một video quảng cáo hoặc sản phẩm, một video âm nhạc trên bài hát của bạn, một bộ phim giống một video tham chiếu, một bản dựng từ tư liệu của chính bạn, một bộ phim mới trong một định dạng đã lưu, một vòng xem qua các phong cách. Hoặc chỉ cần nói điều bạn muốn ("make a music video for this song"); agent đi đúng đường.

**Tôi nên chọn chế độ nào?** Quick mode khi bạn muốn một bộ phim hoàn chỉnh ngay hôm nay hoặc đăng thường xuyên; Film mode khi một tác phẩm phải tốt hết mức có thể. Agent gợi ý một chế độ từ mục tiêu của bạn.

**Một bộ phim mất bao lâu?** Ở Quick mode, một bộ phim 30 giây là một phiên làm việc ngắn: vài câu hỏi, một kế hoạch, hai cảnh để xem, một bản nháp nhanh, rồi kết xuất cuối (mỗi bước vài giây tới vài phút). Ở Film mode, một bộ phim 30 giây thường là vài phiên: phỏng vấn và lộ trình mất vài phút, kịch bản và khung phong cách một buổi ngồi, và việc kết xuất một bộ phim 30 giây mất vài phút trên một GPU gần đây. Phần lớn thời gian đi vào ghi chú của bạn, và đó chính là mục đích.

**Tôi có cần GPU mạnh không?** Bất kỳ máy Mac gần đây nào (Apple silicon) hoặc một PC với driver đồ họa hoạt động đều đủ. Agent kiểm tra điều này lúc bắt đầu (`capture.mjs --probe`). Không có GPU trong Chrome không giao diện, việc kết xuất lùi về CPU: ổn cho kiểm thử, chậm cho cả một bộ phim.

**Tôi có thể dùng tài liệu tham chiếu của chính mình không?** Có: thả hình ảnh vào `refs/` và các liên kết hoặc tên phim kèm mốc thời gian vào `refs/links.txt`. Tài liệu tham chiếu có bản quyền chỉ được dùng để lấy tâm trạng, không bao giờ xuất hiện trong khung hình.

**Tôi có thể dùng phim của mình cho mục đích thương mại (quảng cáo, việc khách hàng, kênh kiếm tiền) không?** Về phía bộ công cụ, có. Mọi phông nó chia hay tìm đều theo một giấy phép cho phép dùng thương mại mà không nợ gì trên màn hình hay trong mô tả (SIL OFL, Apache, MIT, Ubuntu Font Licence, CC0); phông được dùng trong hình ảnh, không bao giờ được bán hay chia sẻ dưới dạng tệp. Bốn mặt chữ tuyển chọn đến từ Fontshare (ITF Free Font License): cũng miễn phí cho công việc thương mại, nhưng bạn tự tải chúng và không bao giờ truyền các tệp đi; bộ công cụ giữ mọi tệp phông ngoài git. Tài liệu tham chiếu do agent tìm chỉ để lấy tâm trạng và hình dạng; một hình ảnh hay một âm thanh chỉ vào bộ phim với một giấy phép cho phép nó, được ghi trong `LICENSES.csv`. Logo, phông thương hiệu, tư liệu và bài hát của chính bạn vẫn là trách nhiệm của bạn. Nhạc và hình ảnh mở: bộ công cụ chỉ lấy tư liệu public domain, CC0 và CC BY, và CC BY-SA cho hình ảnh (CC0 trước cho nhạc), ghi lại mỗi giấy phép và viết phần ghi công cho mô tả video của bạn bên cạnh mỗi bản cuối; hãy kiểm tra trang nguồn của một mục trước khi bạn xuất bản, và giữ tệp ghi công cùng bộ phim (nó trả lời một khiếu nại YouTube Content ID trên một track CC BY). Ai xuất bản một bộ phim thì chịu trách nhiệm về giấy phép của nó; bộ công cụ được cung cấp nguyên trạng (giấy phép MIT). Đây không phải tư vấn pháp lý.

**Tôi viết phần ghi công ở đâu?** Trong mô tả của video (YouTube) hoặc chú thích của bài đăng (Instagram, TikTok, X), không ở đâu trên hình ảnh. Mỗi bản cuối để lại `<title>-credits.txt` bên cạnh bộ phim: dán nó nguyên trạng. Tư liệu public domain và CC0 không cần dòng nào (tệp vẫn liệt kê chúng, ngắn gọn); tư liệu CC BY và CC BY-SA cần dòng của chúng, với liên kết giấy phép mà tệp đã mang theo. Tệp đó cũng là câu trả lời của bạn nếu một nền tảng gắn cờ một track hay một hình ảnh.

**Phim của tôi đi đâu?** Vào thư mục bạn đã khởi động agent trong đó: nếu nó trống hoặc chỉ chứa phim, mỗi bộ phim có một thư mục con riêng ở đó; nếu không (thư mục nhà của bạn, màn hình nền, một dự án code), agent tạo một thư mục `Films` ở đó và giữ mọi bộ phim trong đó. Agent cho bạn biết đường dẫn. Lần sau khởi động agent ở cùng một nơi và "continue" liệt kê các bộ phim của bạn theo tên. Nếu bạn bắt đầu mà không chọn thư mục (một cuộc trò chuyện không có thư mục trong ứng dụng Claude), phim của bạn đi vào một thư mục `Films` trong thư mục nhà của bạn và agent chuyển cuộc trò chuyện vào thư mục của bộ phim, để ảnh tĩnh, nhạc và bản nháp hiện trong cuộc trò chuyện.

**Phim của tôi ở đâu? Tôi có cần git không?** Bộ phim hoàn chỉnh được sao chép vào thư mục phim của bạn dưới tên `<title>.mp4`, và agent cho bạn đường dẫn đó; tệp đó là tất cả những gì bạn cần. Bạn không bao giờ phải chạm vào git: nếu nó được cài, agent giữ một lịch sử cục bộ của các tệp văn bản của bộ phim (để một lần sửa xấu có thể được hoàn tác). Không có gì được tải lên bất cứ đâu, và video không phải là một phần của nó.

**Tôi thích một bộ phim. Bộ phim tiếp theo có thể có cùng định dạng không?** Có. Nói "save the format" ("formatı kaydet") sau bản cuối; lần sau nói "same format" ("aynı formatta"). Diện mạo, chữ, âm thanh, phong cách máy quay và nhịp điệu được giữ, chỉ ý tưởng được hỏi, và các cảnh cùng lời được làm mới cho nó. Các định dạng ở lại trên máy tính của bạn (`~/.cinecode/formats`).

**Một bộ phim dùng bao nhiêu token, và tôi xem nó thế nào?** Một bộ phim là một cuộc trò chuyện dài trong đó agent viết code, kết xuất và kiểm tra: một bộ phim Quick 30–60 giây thường mất 100–250 bước. Mỗi bước đọc lại toàn bộ cuộc trò chuyện; phần lớn trong số đó đến từ bộ nhớ đệm và rẻ, nhưng mỗi bước lớn dần khi cuộc trò chuyện lớn dần. Vì vậy khi một bước xong và cuộc trò chuyện đã lớn, bộ công cụ đề nghị tiếp tục trong một cuộc trò chuyện mới; không có gì bị mất, vì bộ phim sống trong các tệp của nó. `python3 tools/usage.py` trong thư mục phim cho thấy token của mỗi cuộc trò chuyện (Claude Code). Mỗi cuộc trò chuyện cũng bắt đầu với mô tả ngắn của mọi skill đã cài và định nghĩa công cụ của mọi plugin và connector đã kết nối (hướng dẫn đầy đủ của một skill chỉ tải khi nó được dùng); tắt những cái một bộ phim không cần làm cho mỗi bước rẻ hơn.

**Những ngôn ngữ nào?** Agent trả lời bằng ngôn ngữ của bạn. Phụ đề tắt trừ khi bạn yêu cầu (tối đa hai ngôn ngữ, xếp chồng).

**Ngoại tuyến?** Kết xuất, trộn âm và các kiểm tra hoạt động ngoại tuyến, và bộ khởi đầu Quick mode cũng vậy (Canvas 2D, Web Audio); tìm kiếm cần mạng (tài liệu tham chiếu, nhạc, lần tải phông và phong cách đầu tiên, sau đó được lưu đệm). Cảnh three.js cần mạng một lần cho các thư viện của nó (hoặc một bản sao cục bộ, xem `references/looks.md` §6); `starter/index.html` không cần gì cả.

## Kiểm thử

Từ thư mục của bộ công cụ, chạy `python3 -m unittest discover -s tests`; đặt `CINECODE_BROWSER_TESTS=1` ở phía trước cho các kiểm thử Chrome và ffmpeg thật. Bộ kiểm thử cũng chạy ở mỗi lần push trên Windows (có và không có Git và bash) và trên Ubuntu. Nếu có gì trục trặc, hãy báo cáo trên GitHub.

## Ghi công

Được làm bởi Sarp Yıldız ([@sarpstar](https://github.com/sarpstar)) cùng với Claude, trong Claude Code và Cursor. Giấy phép MIT, xem [LICENSE](LICENSE).
Được xây trên [three.js](https://github.com/mrdoob/three.js) (MIT) và [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing) (Zlib), được tải lúc kết xuất, không đóng gói kèm.
Một số ý tưởng lấy cảm hứng từ [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT).
Bộ nhân vật (`references/characters.md`) lấy cảm hứng từ [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) của John Heibel; các kiểm tra sáo ngữ và màu sắc lấy cảm hứng từ một nghiên cứu về các bộ phim trong [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos). Chỉ là ý tưởng: không có code, prompt hay khung hình nào từ cả hai được đưa vào.
Phương pháp lưới nhịp và các bài học về video âm nhạc, âm thanh chuyển cảnh và chữ động đi theo [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills) (MIT), được viết lại cho bộ công cụ này.
Thư viện phong cách (`styles/`) là các công thức phong cách của [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) bởi LemoLab (MIT, `styles/LICENSE-lemo-opuscar`), được ghim ở một commit; phim demo và engine của chúng được liên kết, không đưa vào. Công thức `vox-explainer` là của chính bộ công cụ; các loại cảnh quay và bài học rà soát của nó đi theo [charlie947/motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) (MIT).
Cũng được viết lại cho bộ công cụ này, tất cả đều MIT: danh mục cảnh quay phim sản phẩm theo [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion); các loại nhịp và lý do cắt dựng theo [cth9191/animate](https://github.com/cth9191/animate); các quy tắc đường nối cắt, điểm nảy một khung hình và kiểm tra vòng lặp, nhòe chuyển động chỉ ở nơi sự vật chuyển động, bài kiểm tra một câu không lời và khung bìa mạng xã hội theo [howseen-ai/claude-motion-design](https://github.com/howseen-ai/claude-motion-design); từ vựng ánh sáng và ống kính theo [showheyohtaki/motion-prompt](https://github.com/showheyohtaki/motion-prompt).
Các nguyên tắc chuyển động (`references/motion.md`) rút ra ý tưởng từ [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) (MIT) và [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) (MIT); ngữ pháp ảnh hero giao diện (`references/craft.md` §8) trên ý tưởng từ [1weiho/cinematic-shot](https://github.com/1weiho/cinematic-shot) (MIT); nhịp độ chính xác theo khung hình trên [cth9191/animate](https://github.com/cth9191/animate) (MIT); phần dựng tư liệu (`references/footage-edit.md`) trên các ngưỡng khoảng lặng và quay lại cùng nhịp theo lời nói từ [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) (MIT) và mật độ đồ họa theo thời gian lời nói từ [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) (MIT). Các nhạc cụ thu sẵn (`scripts/samples.py`) là [Versilian Community Sample Library](https://github.com/sgossner/VCSL) CC0 như được đóng gói bởi [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (MIT), được lấy theo yêu cầu, không đóng gói kèm; các công thức `line-boil`, `liquid-motion`, `shape-morph`, `sticker-explainer` và `variety-captions` cùng bài kiểm tra ban giám khảo đi theo ghi chú phong cách và vòng rà soát của nó, được viết lại cho bộ công cụ này. Các kiểm tra trên lời của bộ phim (`scripts/words_check.py`) đi theo các họ mẫu của [blader/humanizer](https://github.com/blader/humanizer) (MIT) và [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) của Wikipedia, với các tương đương tiếng Thổ Nhĩ Kỳ. Ngoài các công thức lemo-opuscar (được đưa vào theo giấy phép MIT của chúng), tất cả đều được viết bằng lời của chúng tôi; không có code hay văn bản nào bị sao chép. Các mặt chữ tùy chọn đến từ [Fontsource](https://fontsource.org) (code MIT; mỗi phông giữ giấy phép của riêng nó, phần lớn là SIL OFL 1.1), được tải lúc kết xuất. `fonts.py` đọc [Fontsource API](https://fontsource.org/docs/api) và danh sách thẻ công khai của [google/fonts](https://github.com/google/fonts) lúc chạy; cả hai đều không đóng gói kèm.
Các nhạc cụ thu sẵn là CC0: [Versilian Community Sample Library](https://github.com/sgossner/VCSL) và [Versilian Studios Chamber Orchestra 2 Community Edition](https://github.com/sgossner/VSCO-2-CE), chỉ được lấy từng phần nhỏ khi một bộ phim dùng chúng.
Các hiệu ứng âm thanh làm sẵn là các gói âm thanh (CC0) của [Kenney](https://kenney.nl), được tải xuống một lần khi một bộ phim lần đầu cần chúng.
Các giọng tiếng Thổ Nhĩ Kỳ miễn phí được gợi ý trong phần Yêu cầu: EMA Lightning (Canberk Aslan), VoxCPM2 Türkçe ses tasarımı (alexturkey) và Ahenk (Özgür Güler); cảm ơn các tác giả của chúng.
Repository: [github.com/sarpstar/cinecode](https://github.com/sarpstar/cinecode)

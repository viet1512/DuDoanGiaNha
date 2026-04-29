function makePrediction() {
  const data = {
      chieuDai: parseFloat(document.getElementById("chieuDai").value),
      chieuNgang: parseFloat(document.getElementById("chieuNgang").value),
      dienTich: parseFloat(document.getElementById("dienTich").value),
      Phongngu: parseInt(document.getElementById("Phongngu").value),
      SoTang: parseFloat(document.getElementById("SoTang").value),
      PhongTam: parseFloat(document.getElementById("PhongTam").value),
      Loai: document.getElementById("Loai").value,
      GiayTo: document.getElementById("GiayTo").value,
      TinhTrangNoiThat: document.getElementById("TinhTrangNoiThat").value,
      Phuong: document.getElementById("Phuong").value
  };

  fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    if (result.error) {
      document.getElementById("result").innerText = `Không thể tính toán: ${result.error}`;
      return;
    }

    const riskText = translateRisk(result.risk_level);
    const liquidityText = translateLiquidity(result.liquidity_level);
    const adjustmentText = formatAdjustmentPercent(result.adjustment_percent);

    document.getElementById("result").innerHTML = `
      <p><strong>Mức giá ước tính ban đầu:</strong> ${formatMoney(result.ml_price)}</p>
      <p><strong>Mức giá gợi ý sau khi xét thêm yếu tố thực tế:</strong> ${formatMoney(result.final_price)}</p>
      <p><strong>Khoảng giá tham khảo:</strong> ${formatMoney(result.price_range.min)} – ${formatMoney(result.price_range.max)}</p>
      <p><strong>Mức điều chỉnh so với bước ước tính ban đầu:</strong> ${adjustmentText}</p>
      <p><strong>Đánh giá rủi ro:</strong> ${riskText}</p>
      <p><strong>Mức dễ mua/bán (thanh khoản):</strong> ${liquidityText}</p>
      <p class="muted small">Lưu ý: đây là công cụ hỗ trợ tham khảo, không thay thế thẩm định chuyên nghiệp hoặc kiểm tra pháp lý tại chỗ.</p>
    `;

    renderList("rulesList", (result.fired_rules || []).map(humanizeFiredRule), "Hiện chưa có yếu tố đặc biệt nào được hệ thống nhấn mạnh.");
    renderList("warningsList", (result.warnings || []).map(humanizeWarning), "Không có cảnh báo đặc biệt.");
    renderList("recommendationsList", result.recommendations || [], "Chưa có gợi ý thêm.");
  })
  .catch(error => console.error('Error:', error));
}

function formatMoney(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "—";
  }
  const num = Number(value);
  return `${num.toLocaleString("vi-VN")} VND`;
}

function formatAdjustmentPercent(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "không đổi";
  }
  const num = Number(value);
  if (Math.abs(num) < 1e-9) {
    return "không đổi";
  }
  const rounded = Math.round(num * 100) / 100;
  if (rounded > 0) {
    return `tăng thêm khoảng ${rounded}%`;
  }
  return `giảm khoảng ${Math.abs(rounded)}%`;
}

function translateRisk(level) {
  if (level === "low") return "thấp";
  if (level === "medium") return "trung bình";
  if (level === "high") return "cao";
  return "chưa xác định rõ";
}

function translateLiquidity(level) {
  if (level === "low") return "thấp (có thể khó bán nhanh hoặc cần thời gian tìm người mua)";
  if (level === "medium") return "trung bình";
  if (level === "high") return "cao (thường dễ giao dịch hơn nếu các điều kiện khác ổn)";
  return "chưa xác định rõ";
}

function humanizeFiredRule(rule) {
  if (!rule) {
    return "";
  }
  return rule.description || "";
}

function humanizeWarning(warning) {
  const text = String(warning || "").trim();
  if (!text) {
    return "";
  }
  return text.replace(/^Cảnh báo:\s*/i, "");
}

function renderList(elementId, items, emptyText) {
  const target = document.getElementById(elementId);
  target.innerHTML = "";
  const cleaned = (items || []).map(item => String(item).trim()).filter(Boolean);
  if (cleaned.length === 0) {
    const li = document.createElement("li");
    li.className = "muted";
    li.innerText = emptyText || "Không có thông tin.";
    target.appendChild(li);
    return;
  }
  cleaned.forEach(item => {
    const li = document.createElement("li");
    li.innerText = item;
    target.appendChild(li);
  });
}

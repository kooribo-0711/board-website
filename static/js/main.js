function previewImage(input) {
  const preview = document.getElementById('preview');
  const file = input.files[0];

  if (!file) return;

  const reader = new FileReader();
  reader.onload = e => {
    preview.src = e.target.result;
    preview.style.display = 'block';
  };
  reader.readAsDataURL(file);
}

// 마우스 움직임 Y2K 배경 효과
document.addEventListener("mousemove", e => {
  document.body.style.backgroundPosition =
    `${e.clientX / 15}px ${e.clientY / 15}px`;
});

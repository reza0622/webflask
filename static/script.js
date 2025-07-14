// untuk menampilkan semua elemen berita ketika tombol "Lihat Semua" diklik
document.querySelectorAll('.toggle-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    const source = this.dataset.target;
    const items = document.querySelectorAll(`.berita-${source}`);
    const card = btn.closest('.card');
    let expanded = this.getAttribute('data-expanded') === 'true';

    items.forEach(function (item, index) {
      if (index >= 4) {
        item.style.display = expanded ? 'none' : 'list-item';
      }
    });

    // Toggle tinggi card
    if (expanded) {
      card.classList.remove('expand');
    } else {
      card.classList.add('expand');
    }

    this.setAttribute('data-expanded', !expanded);
    this.textContent = expanded ? 'Lihat Semua' : 'Sembunyikan';
  });
});

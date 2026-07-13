# 🎨 AEOS Frontend & UI Guidelines (DaisyUI Edition)

### Semantic Styling Over Utility Bloat
- Hindari menulis kelas utility Tailwind yang panjang untuk kontrol dasar.
- **Standar DaisyUI**: Gunakan kelas semantik:
  - Button: `btn btn-primary`
  - Alert: `alert alert-error`
  - Card: `card bg-base-100 shadow-xl`
  - Modal: `modal` + `modal-box`
- Tambahkan kelas utility hanya untuk spacing halus (`btn btn-primary w-full mt-4`).

### Theme Token Rule
- Jangan gunakan kode warna HEX/RGB hardcoded (misal `bg-[#3b82f6]`).
- Gunakan token warna tema bawaan DaisyUI:
  - Backgrounds: `bg-base-100` (utama), `bg-base-200` (container), `bg-base-300` (nested).
  - Text colors: `text-primary`, `text-secondary`, `text-base-content`.
  - State colors: `btn-info`, `btn-success`, `btn-warning`, `btn-error`.

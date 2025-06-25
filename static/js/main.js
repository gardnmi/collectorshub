import '@/css/main.css';
import htmx from 'htmx.org';
import imageCompression from 'browser-image-compression';


// Make HTMX available globally
window.htmx = htmx;

// Client-side image compression for file inputs named 'images'
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      // Only process forms with file input named 'images'
      const fileInputs = form.querySelectorAll('input[type="file"][name="images"]');
      if (!fileInputs.length) return;
      let changed = false;
      for (const input of fileInputs) {
        if (!input.files || !input.files.length) continue;
        const files = Array.from(input.files);
        const compressedFiles = [];
        for (const file of files) {
          // Only compress if >2MB
          if (file.size > 2 * 1024 * 1024) {
            try {
              const compressed = await imageCompression(file, {
                maxSizeMB: 2,
                maxWidthOrHeight: 3000, // optional, limit pixel size
                useWebWorker: true,
                initialQuality: 0.7,
              });
              compressedFiles.push(compressed);
              changed = true;
            } catch (err) {
              console.error('Image compression failed:', err);
              compressedFiles.push(file); // fallback to original
            }
          } else {
            compressedFiles.push(file);
          }
        }
        if (changed) {
          // Replace FileList with new DataTransfer
          const dt = new DataTransfer();
          compressedFiles.forEach(f => dt.items.add(f));
          input.files = dt.files;
        }
      }
    });
  });
});
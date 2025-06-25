import '@/css/main.css';
import htmx from 'htmx.org';
import imageCompression from 'browser-image-compression';

// Make HTMX available globally
window.htmx = htmx;

// Helper: Promise with timeout
function promiseWithTimeout(promise, ms) {
  let timeout;
  const timeoutPromise = new Promise((_, reject) => {
    timeout = setTimeout(() => reject(new Error('Compression timed out')), ms);
  });
  return Promise.race([
    promise.finally(() => clearTimeout(timeout)),
    timeoutPromise
  ]);
}

// Client-side image compression for file inputs named 'images'
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      // If the submitter is a delete button, skip compression and allow default
      if (e.submitter && e.submitter.name && e.submitter.name.startsWith('delete_image_')) {
        return; // allow default submit for delete
      }
      // Show spinner on the submit button
      let submitBtn = e.submitter || form.querySelector('button[type="submit"],input[type="submit"]');
      let originalBtnContent;
      if (submitBtn) {
        originalBtnContent = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading loading-spinner loading-sm"></span> Processing...';
      }
      e.preventDefault(); // Always prevent default for uploads
      if (form._submitting) {
        console.log('Form already submitting, skipping duplicate submit.');
        return;
      }
      form._submitting = true;
      // Only process forms with file input named 'images'
      const fileInputs = form.querySelectorAll('input[type="file"][name="images"]');
      if (!fileInputs.length) {
        setTimeout(() => form.submit(), 0);
        return;
      }
      let changed = false;
      for (const input of fileInputs) {
        if (!input.files || !input.files.length) {
          console.log('No files found in input:', input);
          continue;
        }
        const files = Array.from(input.files);
        console.log(`Found ${files.length} file(s) in input[name="${input.name}"]`);
        const compressedFiles = [];
        for (const file of files) {
          console.log(`Processing file: ${file.name}, type: ${file.type}, size: ${(file.size/1024/1024).toFixed(2)}MB`);
          // Only compress if >2MB
          if (file.size > 2 * 1024 * 1024) {
            try {
              console.log(`Compressing ${file.name}: original size ${(file.size/1024/1024).toFixed(2)}MB`);
              let compressed = await promiseWithTimeout(
                imageCompression(file, {
                  maxSizeMB: 2,
                  maxWidthOrHeight: 1500, // lower for faster/surer compression
                  useWebWorker: true,
                  initialQuality: 0.7,
                }),
                10000 // 10 seconds
              );
              // Ensure we have a File, not just a Blob
              if (!(compressed instanceof File)) {
                compressed = new File([compressed], file.name, { type: compressed.type || file.type });
                console.log(`Wrapped compressed blob as File: ${compressed.name}, type: ${compressed.type}`);
              }
              console.log(`Compressed ${file.name}: new size ${(compressed.size/1024/1024).toFixed(2)}MB, type: ${compressed.type}`);
              compressedFiles.push(compressed);
              changed = true;
            } catch (err) {
              console.error(`Image compression failed for ${file.name}:`, err);
              console.warn(`Falling back to original file for ${file.name}`);
              compressedFiles.push(file); // fallback to original
            }
          } else {
            console.log(`Skipping compression for ${file.name} (size <= 2MB)`);
            compressedFiles.push(file);
          }
        }
        if (changed) {
          console.log(`Replacing FileList for input[name="${input.name}"] with ${compressedFiles.length} file(s)`);
          const dt = new DataTransfer();
          compressedFiles.forEach(f => dt.items.add(f));
          input.files = dt.files;
          // Log the files that will be submitted
          Array.from(input.files).forEach(f =>
            console.log(`Will submit file: ${f.name}, size: ${(f.size/1024/1024).toFixed(2)}MB, type: ${f.type}`)
          );
        }
      }
      // Always submit the form after processing
      setTimeout(() => {
        // Do NOT restore the button content here; keep spinner/Processing until page reload
        form.submit();
      }, 0);
    });
  });
});
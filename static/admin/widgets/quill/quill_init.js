(function () {
  function init(textarea) {
    if (textarea.dataset.quillReady) return;
    textarea.dataset.quillReady = "1";

    const wrapper = document.createElement("div");
    wrapper.className = "quill-holder";
    const editor = document.createElement("div");
    wrapper.appendChild(editor);
    textarea.parentNode.insertBefore(wrapper, textarea);

    const quill = new Quill(editor, {
        theme: "snow",
          modules: {
            toolbar: [
              [{ header: [1, 2, 3, 4, 5, 6, false] }],
              ["bold", "italic", "underline", "strike"],
              [{ list: "ordered" }, { list: "bullet" }],
              ["link"],
              ["clean"],
            ],
          },
    });
    quill.clipboard.dangerouslyPasteHTML(textarea.value || "");
    quill.on("text-change", function () {
      const html = quill.root.innerHTML;
      textarea.value = (html === "<p><br></p>") ? "" : html;
    });
  }
  function initAll(root) {
    (root || document).querySelectorAll("textarea.quill-html").forEach(init);
  }
  document.addEventListener("DOMContentLoaded", () => initAll(document));
  document.addEventListener("formset:added", (e) => initAll(e.target));
})();
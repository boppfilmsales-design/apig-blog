/* Interactive behaviour for the APIG bilingual site: mobile menu,
   catalogue filtering / search, product gallery switching. */
(function () {
  "use strict";

  // ------------------------------------------------------------ mobile nav
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", nav.classList.contains("open") ? "true" : "false");
    });
  }

  // ------------------------------------------- catalogue filter + search
  var filterRoot = document.querySelector("[data-filter-root]");
  if (filterRoot) {
    var buttons = Array.prototype.slice.call(filterRoot.querySelectorAll("[data-cat]"));
    var cards = Array.prototype.slice.call(filterRoot.querySelectorAll("[data-item]"));
    var search = filterRoot.querySelector("[data-search]");
    var counter = document.querySelector("[data-count]");
    var empty = document.querySelector("[data-empty]");
    var active = "all";

    function apply() {
      var term = (search && search.value || "").trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (card) {
        var catOk = active === "all" || card.getAttribute("data-cat") === active;
        var text = (card.getAttribute("data-search-text") || "").toLowerCase();
        var termOk = !term || text.indexOf(term) !== -1;
        var visible = catOk && termOk;
        card.style.display = visible ? "" : "none";
        if (visible) shown++;
      });
      if (counter) counter.textContent = shown;
      if (empty) empty.style.display = shown ? "none" : "";
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) { b.classList.remove("on"); });
        btn.classList.add("on");
        active = btn.getAttribute("data-cat") || "all";
        apply();
      });
    });

    if (search) {
      var timer = null;
      search.addEventListener("input", function () {
        if (timer) clearTimeout(timer);
        timer = setTimeout(apply, 120);
      });
    }
    apply();
  }

  // -------------------------------------------------- product gallery swap
  var gallery = document.querySelector("[data-gallery]");
  if (gallery) {
    var main = gallery.querySelector("[data-gallery-main]");
    var thumbs = Array.prototype.slice.call(gallery.querySelectorAll("[data-gallery-thumb]"));
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () {
        var src = t.getAttribute("data-src");
        var alt = t.getAttribute("data-alt") || "";
        if (main && src) {
          main.setAttribute("src", src);
          main.setAttribute("alt", alt);
        }
        thumbs.forEach(function (x) { x.classList.remove("on"); });
        t.classList.add("on");
      });
    });
  }

  // ------------------------------------------------- table of contents (EN)
  var toc = document.querySelector("[data-toc]");
  if (toc) {
    var headings = Array.prototype.slice.call(
      document.querySelectorAll(".prose h2")
    );
    if (headings.length) {
      var list = document.createElement("ul");
      headings.forEach(function (h) {
        var slug = h.textContent.trim().toLowerCase()
          .replace(/[^\w\u4e00-\u9fa5]+/g, "-")
          .replace(/^-+|-+$/g, "");
        h.id = slug;
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + slug;
        a.textContent = h.textContent.trim();
        li.appendChild(a);
        list.appendChild(li);
      });
      toc.appendChild(list);
    }
  }
  // ------------------------------------------------------ language choice
  // The bare domain lands on the English site. When a visitor explicitly
  // picks a language, remember it so the root gateway honours that choice
  // instead of guessing again.
  var langLinks = document.querySelectorAll("[data-apig-lang]");
  Array.prototype.forEach.call(langLinks, function (link) {
    link.addEventListener("click", function () {
      try {
        localStorage.setItem("apig_lang", link.getAttribute("data-apig-lang"));
      } catch (e) {
        /* private mode - the gateway falls back to English */
      }
    });
  });

})();

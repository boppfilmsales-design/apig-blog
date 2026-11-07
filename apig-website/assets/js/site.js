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
    // The card grid lives outside .filter-bar, so scope the card lookup to
    // the enclosing catalogue section rather than to the filter bar itself.
    var scope = filterRoot.closest("[data-catalogue]") || filterRoot.parentNode;
    var buttons = Array.prototype.slice.call(filterRoot.querySelectorAll("[data-cat]"));
    var cards = Array.prototype.slice.call(scope.querySelectorAll("[data-item]"));
    var searchInput = filterRoot.querySelector("[data-search]");
    var counter = document.querySelector("[data-count]");
    var empty = document.querySelector("[data-empty]");
    var pager = document.querySelector("[data-pager]");
    var pagerList = document.querySelector("[data-pager-list]");
    var pagerInfo = document.querySelector("[data-pager-info]");
    var active = "all";
    var page = 1;
    var perPage = parseInt(document.documentElement.getAttribute("data-per-page"), 10) || 24;
    var root = document.documentElement;
    var labels = {
      prev: root.getAttribute("data-label-prev") || "Previous",
      next: root.getAttribute("data-label-next") || "Next",
      page: root.getAttribute("data-label-page") || "Page",
      info: root.getAttribute("data-label-info") ||
        "Showing {from}-{to} of {total} results"
    };
    function fill(template, values) {
      return template.replace(/\{(\w+)\}/g, function (whole, key) {
        return values.hasOwnProperty(key) ? values[key] : whole;
      });
    }

    function matches(card) {
      var catOk = active === "all" || card.getAttribute("data-cat") === active;
      var text = (card.getAttribute("data-search-text") || "").toLowerCase();
      var term = (searchInput && searchInput.value || "").trim().toLowerCase();
      var termOk = !term || text.indexOf(term) !== -1;
      return catOk && termOk;
    }

    function syncUrl() {
      if (!window.history || !window.history.replaceState) return;
      var url = new URL(window.location.href);
      if (page > 1) url.searchParams.set("page", String(page));
      else url.searchParams.delete("page");
      if (active !== "all") url.searchParams.set("cat", active);
      else url.searchParams.delete("cat");
      window.history.replaceState(null, "", url.toString());
    }

    function buildPager(total, totalPages) {
      if (!pager || !pagerList) return;
      pagerList.innerHTML = "";
      if (totalPages <= 1) {
        pager.hidden = true;
        if (pagerInfo) pagerInfo.textContent = "";
        return;
      }
      pager.hidden = false;

      function add(label, target, opts) {
        opts = opts || {};
        var b = document.createElement("button");
        b.type = "button";
        b.className = "pager-btn" + (opts.on ? " on" : "");
        b.textContent = label;
        if (opts.disabled) {
          b.disabled = true;
        } else {
          b.addEventListener("click", function () {
            page = target;
            render();
            var anchor = document.querySelector(".grid");
            if (anchor) {
              var top = anchor.getBoundingClientRect().top + window.pageYOffset - 90;
              window.scrollTo({ top: top, behavior: "smooth" });
            }
          });
        }
        if (opts.aria) b.setAttribute("aria-label", opts.aria);
        pagerList.appendChild(b);
      }

      add(labels.prev, page - 1, { disabled: page === 1, aria: labels.prev });

      // Windowed page numbers: first, last, and a band around the current page.
      var nums = [];
      for (var i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || Math.abs(i - page) <= 1) nums.push(i);
      }
      var last = 0;
      nums.forEach(function (n) {
        if (last && n - last > 1) {
          var gap = document.createElement("span");
          gap.className = "pager-gap";
          gap.textContent = "...";
          pagerList.appendChild(gap);
        }
        add(String(n), n, { on: n === page, aria: fill(labels.page, { n: n }) });
        last = n;
      });

      add(labels.next, page + 1, { disabled: page === totalPages, aria: labels.next });

      if (pagerInfo) {
        var from = (page - 1) * perPage + 1;
        var to = Math.min(page * perPage, total);
        pagerInfo.textContent = fill(labels.info, {
          from: from, to: to, total: total, pages: totalPages, page: page
        });
      }
    }

    function render() {
      var matched = [];
      cards.forEach(function (card) {
        if (matches(card)) matched.push(card);
        else card.style.display = "none";
      });

      var total = matched.length;
      var totalPages = Math.max(1, Math.ceil(total / perPage));
      if (page > totalPages) page = totalPages;

      matched.forEach(function (card, index) {
        var onPage = index >= (page - 1) * perPage && index < page * perPage;
        card.style.display = onPage ? "" : "none";
      });

      if (counter) counter.textContent = total;
      if (empty) empty.style.display = total ? "none" : "";
      buildPager(total, totalPages);
      syncUrl();
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) { b.classList.remove("on"); });
        btn.classList.add("on");
        active = btn.getAttribute("data-cat") || "all";
        page = 1;
        render();
      });
    });

    if (searchInput) {
      var timer = null;
      searchInput.addEventListener("input", function () {
        if (timer) clearTimeout(timer);
        timer = setTimeout(function () {
          page = 1;
          render();
        }, 120);
      });
    }

    // Restore state from the URL so a shared link opens the right page.
    var params = new URL(window.location.href).searchParams;
    var wantedCat = params.get("cat");
    var wantedPage = parseInt(params.get("page"), 10);
    if (wantedCat) {
      for (var k = 0; k < buttons.length; k++) {
        if (buttons[k].getAttribute("data-cat") === wantedCat) {
          buttons.forEach(function (b) { b.classList.remove("on"); });
          buttons[k].classList.add("on");
          active = wantedCat;
          break;
        }
      }
    }
    if (wantedPage > 0) page = wantedPage;

    render();
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

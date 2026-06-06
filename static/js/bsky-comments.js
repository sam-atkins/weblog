(function () {
  const HOST = document.getElementById("bsky-comments-host");
  if (!HOST) return;
  const RAW_URI = HOST.dataset.threadUri;
  if (!RAW_URI) return;

  const API_BASE = "https://public.api.bsky.app/xrpc";

  function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString("en-GB", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  function escapeHtml(text) {
    const el = document.createElement("div");
    el.textContent = text;
    return el.innerHTML;
  }

  function renderFacetedText(record) {
    if (!record.facets || !record.facets.length) {
      return escapeHtml(record.text);
    }
    const facets = record.facets.sort(
      (a, b) => a.index.byteStart - b.index.byteStart,
    );
    const bytes = record.text;
    let result = "";
    let pos = 0;

    for (const facet of facets) {
      const start = facet.index.byteStart;
      const end = facet.index.byteEnd;
      if (start > pos) {
        result += escapeHtml(bytes.slice(pos, start));
      }
      const segment = escapeHtml(bytes.slice(start, end));
      const feature = facet.features[0];
      if (feature.$type === "app.bsky.richtext.facet#link") {
        result += `<a href="${escapeHtml(feature.uri)}" target="_blank" rel="noopener">${segment}</a>`;
      } else if (feature.$type === "app.bsky.richtext.facet#mention") {
        result += `<a href="https://bsky.app/profile/${escapeHtml(feature.did)}" target="_blank" rel="noopener">${segment}</a>`;
      } else if (feature.$type === "app.bsky.richtext.facet#tag") {
        result += `<a href="https://bsky.app/hashtag/${escapeHtml(feature.tag)}" target="_blank" rel="noopener">${segment}</a>`;
      } else {
        result += segment;
      }
      pos = end;
    }
    if (pos < bytes.length) {
      result += escapeHtml(bytes.slice(pos));
    }
    return result;
  }

  function createCommentEl(post, depth) {
    const author = post.author;
    const record = post.record;
    const textHtml = renderFacetedText(record);

    const article = document.createElement("article");
    article.className = "comment";
    if (depth > 0) article.classList.add("nested");

    article.innerHTML = `
      <div class="comment-avatar">
        <img src="${author.avatar || ""}" alt="" width="36" height="36" loading="lazy" onerror="this.style.display='none'">
      </div>
      <div class="comment-body">
        <div class="comment-author">
          <a href="https://bsky.app/profile/${escapeHtml(author.did)}" target="_blank" rel="noopener">
            ${escapeHtml(author.displayName || author.handle)}
          </a>
          <span class="comment-handle">@${escapeHtml(author.handle)}</span>
          <span class="comment-date">${formatDate(record.createdAt)}</span>
        </div>
        <div class="comment-text">${textHtml}</div>
      </div>
    `;

    return article;
  }

  function renderThread(thread, depth, container) {
    if (!thread) return;

    const post = thread.post;
    if (!post) return;

    const el = createCommentEl(post, depth);
    container.appendChild(el);

    if (thread.replies && thread.replies.length > 0) {
      const repliesContainer = document.createElement("div");
      repliesContainer.className = "replies";
      el.appendChild(repliesContainer);

      for (const reply of thread.replies) {
        renderThread(reply, depth + 1, repliesContainer);
      }
    }
  }

  function renderAllComments(thread) {
    const root = document.createElement("div");
    root.className = "bsky-comments";

    if (thread.replies && thread.replies.length > 0) {
      for (const reply of thread.replies) {
        renderThread(reply, 0, root);
      }
    } else {
      root.innerHTML =
        '<p class="bsky-empty">No comments yet. <a href="' +
        escapeHtml(RAW_URI) +
        '" target="_blank" rel="noopener">Reply on Bluesky</a> to add one.</p>';
    }

    root.innerHTML +=
      '<p class="bsky-footer">💬 <a href="' +
      escapeHtml(RAW_URI) +
      '" target="_blank" rel="noopener">Reply on Bluesky</a></p>';

    return root;
  }

  function injectStyles(shadowRoot) {
    const css = `
      :host {
        display: block;
        margin: 2rem 0;
      }
      .bsky-comments {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 0.95rem;
        line-height: 1.5;
        color: #333;
      }
      .comment {
        display: flex;
        gap: 0.6rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e5e7eb;
      }
      .comment:last-child {
        border-bottom: none;
      }
      .comment.nested {
        padding-left: 2.5rem;
      }
      .replies .comment:first-child {
        padding-top: 0.75rem;
      }
      .comment-avatar {
        flex-shrink: 0;
      }
      .comment-avatar img {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #e5e7eb;
      }
      .comment-body {
        flex: 1;
        min-width: 0;
      }
      .comment-author {
        display: flex;
        align-items: baseline;
        gap: 0.4rem;
        flex-wrap: wrap;
      }
      .comment-author a {
        font-weight: 600;
        color: #2563eb;
        text-decoration: none;
      }
      .comment-author a:hover {
        text-decoration: underline;
      }
      .comment-handle {
        color: #9ca3af;
        font-size: 0.85rem;
      }
      .comment-date {
        color: #9ca3af;
        font-size: 0.8rem;
        margin-left: auto;
      }
      .comment-text {
        margin-top: 0.2rem;
        word-break: break-word;
      }
      .comment-text a {
        color: #2563eb;
        text-decoration: underline;
      }
      .bsky-empty {
        color: #6b7280;
        font-style: italic;
      }
      .bsky-footer {
        margin-top: 1rem;
        font-size: 0.85rem;
        text-align: right;
      }
      .bsky-footer a {
        color: #2563eb;
        text-decoration: none;
      }
      .bsky-footer a:hover {
        text-decoration: underline;
      }
    `;
    const style = document.createElement("style");
    style.textContent = css;
    shadowRoot.appendChild(style);
  }

  async function normalizeUri(raw) {
    if (raw.startsWith("at://")) return raw;

    const match = raw.match(/profile\/([^/]+)\/post\/([^/]+)/);
    if (match) {
      let did = match[1];
      const rkey = match[2];
      if (!did.startsWith("did:")) {
        const res = await fetch(
          API_BASE +
            "/app.bsky.actor.getProfile?actor=" +
            encodeURIComponent(did),
        );
        if (!res.ok) throw new Error("Failed to resolve handle");
        const profile = await res.json();
        did = profile.did;
      }
      return "at://" + did + "/app.bsky.feed.post/" + rkey;
    }
    throw new Error("Invalid Bluesky thread URI");
  }

  async function loadComments() {
    try {
      const atUri = await normalizeUri(RAW_URI);
      const res = await fetch(
        API_BASE +
          "/app.bsky.feed.getPostThread?uri=" +
          encodeURIComponent(atUri),
      );
      if (!res.ok) throw new Error("API request failed");
      const data = await res.json();

      HOST.innerHTML = "";

      const shadow = HOST.attachShadow({ mode: "open" });
      injectStyles(shadow);
      const content = renderAllComments(data.thread);
      shadow.appendChild(content);
    } catch (err) {
      HOST.innerHTML =
        '<p style="color:#6b7280;font-style:italic;">Could not load comments.</p>';
    }
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            observer.disconnect();
            loadComments();
          }
        }
      },
      { rootMargin: "300px" },
    );
    observer.observe(HOST);
  } else {
    loadComments();
  }
})();

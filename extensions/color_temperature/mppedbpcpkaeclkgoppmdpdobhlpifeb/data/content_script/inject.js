var background = (function () {
  let tmp = {};
  /*  */
  chrome.runtime.onMessage.addListener(function (request) {
    for (let id in tmp) {
      if (tmp[id] && (typeof tmp[id] === "function")) {
        if (request.path === "background-to-page") {
          if (request.method === id) {
            tmp[id](request.data);
          }
        }
      }
    }
  });
  /*  */
  return {
    "receive": function (id, callback) {
      tmp[id] = callback;
    },
    "send": function (id, data) {
      chrome.runtime.sendMessage({
        "method": id, 
        "data": data,
        "path": "page-to-background"
      }, function () {
        return chrome.runtime.lastError;
      });
    }
  }
})();

var config = {
  "hostname": '',
  "whitelist": [],
  "action": function (e) {
    const R = e.R;
    const G = e.G;
    const B = e.B;
    const A = e.A;
    const mode = e.mode;
    /*  */
    if (window === window.top) {
      if ("whitelist" in e) config.whitelist = e.whitelist;
      if ("top" in e) config.hostname = (new URL(e.top).hostname).replace("www.", '');
      /*  */
      const root = document.documentElement;
      const target = document.querySelector(".ct-class");
      const action = config.hostname ? config.whitelist.indexOf(config.hostname) === -1 : true;
      /*  */
      if (target) target.remove();
      root.style.removeProperty("--ct-R");
      root.style.removeProperty("--ct-G");
      root.style.removeProperty("--ct-B");
      root.style.removeProperty("--ct-A");
      /*  */
      if (action) {
        if (mode === "OFF") {
          const overlay = document.createElement("div");
          overlay.setAttribute("class", "ct-class");
          overlay.setAttribute("mode", mode);
          /*  */
          root.style.setProperty("--ct-R", R);
          root.style.setProperty("--ct-G", G);
          root.style.setProperty("--ct-B", B);
          root.style.setProperty("--ct-A", A / 100);
          root.insertBefore(overlay, root.firstChild);
        }
      }
    }
  }
};

background.send("storage");
background.receive("storage", config.action);
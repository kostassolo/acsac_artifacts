var background = {
  "port": null,
  "message": {},
  "receive": function (id, callback) {
    if (id) {
      background.message[id] = callback;
    }
  },
  "send": function (id, data) {
    if (id) {
      chrome.runtime.sendMessage({
        "method": id,
        "data": data,
        "path": "popup-to-background"
      }, function () {
        return chrome.runtime.lastError;
      });
    }
  },
  "connect": function (port) {
    chrome.runtime.onMessage.addListener(background.listener); 
    /*  */
    if (port) {
      background.port = port;
      background.port.onMessage.addListener(background.listener);
      background.port.onDisconnect.addListener(function () {
        background.port = null;
      });
    }
  },
  "post": function (id, data) {
    if (id) {
      if (background.port) {
        background.port.postMessage({
          "method": id,
          "data": data,
          "path": "popup-to-background",
          "port": background.port.name
        });
      }
    }
  },
  "listener": function (e) {
    if (e) {
      for (let id in background.message) {
        if (background.message[id]) {
          if ((typeof background.message[id]) === "function") {
            if (e.path === "background-to-popup") {
              if (e.method === id) {
                background.message[id](e.data);
              }
            }
          }
        }
      }
    }
  }
};

var config = {
  "global": {
    'B': 41,
    'G': 147,
    'R': 255,
    'A': 100,
    "mode": "ON"
  },
  "send": function () {
    const tmp = {
      "R": config.global.R, 
      "G": config.global.G, 
      "B": config.global.B, 
      "A": config.global.A, 
      "mode": config.global.mode
    };
    /*  */
    background.send("store", tmp);
  },
  "toggle": function (state) {
    document.querySelector(".power").setAttribute("state", state);
    /*  */
    if (state === "ON") {
      str = "No Color Temperature (Ctrl+Shift+Y)";
    } else {
      const red = "Red " + config.global.R;
      const blue = "Blue " + config.global.B;
      const green = "Green " + config.global.G;
      const opacity = "Opacity " + config.global.A;
      str = "Color Temperature: " + red + ', ' + green + ', ' + blue + ', ' + opacity + "%"
    }
    /*  */
    document.getElementById("info-td").textContent = str;
  },
  "handle": {
    "click": function (e) {
      const state = e.target.getAttribute("state");
      /*  */
      config.global.mode = state === "ON" ? "OFF" : "ON";
      config.toggle(config.global.mode);
      config.send();
    },
    "change": function (e) {
      const id = e.target.getAttribute("id");
      if (id.indexOf("R-") !== -1) config.global.R = e.target.value;
      else if (id.indexOf("G-") !== -1) config.global.G = e.target.value;
      else if (id.indexOf("B-") !== -1) config.global.B = e.target.value;
      else if (id.indexOf("A-") !== -1) config.global.A = e.target.value;
      /*  */
      config.send();
    }
  },
  "load": function () {
    const R = document.getElementById("R-slider");
    const G = document.getElementById("G-slider");
    const B = document.getElementById("B-slider");
    const A = document.getElementById("A-slider");
    /*  */
    const power = document.querySelector(".power");
    const reload = document.getElementById("reload");
    const options = document.getElementById("options");
    const support = document.getElementById("support");
    const donation = document.getElementById("donation");
    const add = document.getElementById("add-whitelist");
    const remove = document.getElementById("remove-whitelist");
    /*  */
    R.addEventListener("input", config.handle.change);
    G.addEventListener("input", config.handle.change);
    B.addEventListener("input", config.handle.change);
    A.addEventListener("input", config.handle.change);
    /*  */
    power.addEventListener("click", config.handle.click);
    reload.addEventListener("click", function () {background.send("reload")});
    options.addEventListener("click", function () {background.send("options")});
    support.addEventListener("click", function () {background.send("support")});
    donation.addEventListener("click", function () {background.send("donation")});
    add.addEventListener("click", function () {background.send("add-whitelist")});
    remove.addEventListener("click", function () {background.send("remove-whitelist")});
    /*  */
    background.receive("storage", function (data) {
      config.global.R = data.R;
      config.global.G = data.G;
      config.global.B = data.B;
      config.global.A = data.A;
      config.global.mode = data.mode;
      /*  */
      R.value = config.global.R;
      G.value = config.global.G;
      B.value = config.global.B;
      A.value = config.global.A;
      /*  */
      config.toggle(config.global.mode);
    });
    /*  */
    background.send("load");
    window.removeEventListener("load", config.load, false);
  }
};

window.addEventListener("load", config.load, false);
background.connect(chrome.runtime.connect({"name": "popup"}));

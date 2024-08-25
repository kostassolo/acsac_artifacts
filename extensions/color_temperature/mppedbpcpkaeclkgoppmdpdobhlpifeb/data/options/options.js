var background = (function () {
  let tmp = {};
  chrome.runtime.onMessage.addListener(function (request) {
    for (let id in tmp) {
      if (tmp[id] && (typeof tmp[id] === "function")) {
        if (request.path === "background-to-options") {
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
        "path": "options-to-background"
      }, function () {
        return chrome.runtime.lastError;
      });
    }
  }
})();

var config = {
  "whiteList": [],
  "connect": function (elem, pref) {
    let att = "value";
    if (elem) {
      if (elem.type === "checkbox") att = "checked";
      if (elem.localName === "span") att = "textContent";
      if (elem.localName === "select") att = "selectedIndex";
      /*  */
      let pref = elem.getAttribute("data-pref");
      background.send("get", pref);
      elem.addEventListener("change", function () {
        background.send("changed", {"pref": pref, "value": this[att]});
      });
    }
    /*  */
    return {
      get value () {return elem[att]},
      set value (val) {
        if (elem.type === "file") return;
        elem[att] = val;
      }
    }
  },
  "load": function () {
    document.getElementById("input-field-add").addEventListener("click", config.interface.add.item);
    document.getElementById("input-field").addEventListener("keypress", function (e) {
      let key = e.which || e.keyCode;
      if (key === 13) config.interface.add.item(e);
    });
    /*  */
    document.getElementById("white-list-table").addEventListener("click", function (e) {
      let tagname = e.target.tagName.toLowerCase();
      let nodename = e.target.nodeName.toLowerCase();
      /*  */
      if (tagname === "td" || nodename === "td") {
        if (e.target.getAttribute("type") === "close") {
          let url = e.target.parentNode.childNodes[1].textContent;
          config.whiteList = config.whiteList.filter(function (e) {
            return e && e !== url;
          });
          /*  */
          config.interface.store();
        }
      }
    });
    /*  */
    let prefs = [...document.querySelectorAll("*[data-pref]")];
    if (prefs && prefs.length) {
      prefs.forEach(function (elem) {
        let pref = elem.getAttribute("data-pref");
        window[pref] = config.connect(elem, pref);
      });
    }
    /*  */
    background.send("white-list");
    window.removeEventListener("load", config.load, false);
  },
  "interface": {
    "store": function () {
      config.interface.fill(config.whiteList);
      background.send("store", {"whiteList": config.whiteList});
    },
    "add": {
      "item": function () {
        let value = document.getElementById("input-field").value;
        let regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        if (value && regexp.test(value)) {
          /*  */
          let a = document.createElement('a');
          a.href = value;
          value = a.host.replace("www.", '');
          a.setAttribute("target", "_blank");
          /*  */
          config.whiteList = config.whiteList.filter(function (e) {return e !== value});
          config.whiteList.push(value);
          config.interface.store();
          /*  */
          document.getElementById("input-field").value = '';
        }
      }
    },
    "fill": function (arr) {
      let count = 1;
      let table = document.getElementById("white-list-table");
      /*  */
      config.whiteList = arr;
      table.textContent = '';
      /*  */
      for (let i = config.whiteList.length - 1; i >= 0; i--) {
        const a = document.createElement('a');
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        const td2 = document.createElement("td");
        const td3 = document.createElement("td");
        /*  */
        td2.appendChild(a);
        td3.textContent = '✕';
        td1.textContent = count;
        td2.setAttribute("type", "item");
        td3.setAttribute("type", "close");
        td1.setAttribute("type", "number");
        /*  */
        a.href = config.whiteList[i];
        a.textContent = config.whiteList[i];
        a.setAttribute("target", "_blank");
        a.setAttribute("href", "https://" + config.whiteList[i]);
        /*  */
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        table.appendChild(tr);
        /*  */
        count++;
      }
    }
  }
};

background.receive("white-list", function (e) {
  config.interface.fill(e.whitelist);
});

background.receive("set", function (o) {
  if (window[o.pref]) {
    window[o.pref].value = o.value;
  }
});

window.addEventListener("load", config.load, false);
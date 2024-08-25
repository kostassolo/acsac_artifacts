var core = {
  "start": function () {
    core.load();
  },
  "install": function () {
    core.load();
  },
  "load": function () {
    app.button.icon(null, config.dimmer.mode);
  },
  "update": {
    "popup": function () {
      app.popup.send("storage", {
        "R": config.dimmer.R,
        "G": config.dimmer.G,
        "B": config.dimmer.B,
        "A": config.dimmer.A,
        "mode": config.dimmer.mode
      });
    },
    "options": function () {
      app.options.send("white-list", {
        "R": config.dimmer.R,
        "G": config.dimmer.G,
        "B": config.dimmer.B,
        "A": config.dimmer.A,
        "mode": config.dimmer.mode,
        "whitelist": config.whitelist.array
      });
    },
    "page": function (e) {
      app.page.send("storage", {
        "R": config.dimmer.R,
        "G": config.dimmer.G,
        "B": config.dimmer.B,
        "A": config.dimmer.A,
        "mode": config.dimmer.mode,
        "whitelist": config.whitelist.array.join('|')
      }, (e && "tabId" in e) ? e.tabId : null, (e && "frameId" in e) ? e.frameId : null);
      /*  */
      app.button.icon(null, config.dimmer.mode);
      core.update.options();
      core.update.popup();
    }
  },
  "action": {
    "storage": function (changes, namespace) {
      /*  */
    },
    "hotkey": {
      "add": function () {
        app.tab.query.active(function (tab) {
          if (tab) {
            if (tab.url) {
              let tmp = config.whitelist.array;
              let hostname = (new URL(tab.url).hostname).replace("www.", '');
              /*  */
              if (tmp.indexOf(hostname) === -1) {
                tmp.push(hostname);
                config.whitelist.array = tmp;
                core.update.page(tab);
              }
            }
          }
        });
      },
      "remove": function () {
        app.tab.query.active(function (tab) {
          if (tab) {
            if (tab.url) {
              let tmp = config.whitelist.array;
              let hostname = (new URL(tab.url).hostname).replace("www.", '');
              /*  */
              if (tmp.indexOf(hostname) !== -1) {
                tmp.splice(tmp.indexOf(hostname), 1);
                config.whitelist.array = tmp;
                core.update.page(tab);
              }
            }
          }
        });
      },
      "pressed": function (e) {
        if (e === "toggle") {
          if (config.hotkey.mode) {
            config.dimmer.mode = config.dimmer.mode === "ON" ? "OFF" : "ON";
            core.update.page();
          }
        } else if (e === "add") {
          if (config.hotkey.add) {
            core.action.hotkey.add();
          }
        } else if (e === "remove") {    
          if (config.hotkey.remove) {
            core.action.hotkey.remove();
          }
        }
        /*  */
        core.update.popup();
      }
    }
  }
};

app.options.receive("store", function (data) {
  config.whitelist.array = data.whiteList;
  core.update.page();
});

app.options.receive("changed", function (o) {
  config.set(o.pref, o.value);
  app.options.send("set", {"pref": o.pref, "value": config.get(o.pref)});
  core.update.page();
});

app.popup.receive("reload", function () {
  app.tab.query.active(function (tab) {
    if (tab) {
      app.tab.reload(tab.id);
    }
  });
});

app.options.receive("get", function (pref) {
  app.options.send("set", {
    "pref": pref, 
    "value": config.get(pref)
  });
});

app.popup.receive("store", function (data) {
  config.dimmer.R = data.R;
  config.dimmer.G = data.G;
  config.dimmer.B = data.B;
  config.dimmer.A = data.A;
  config.dimmer.mode = data.mode;
  /*  */
  core.update.page();
});

app.tab.on.created(core.update.page);
app.tab.on.updated(core.update.page);

app.popup.receive("load", core.update.popup);
app.popup.receive("options", app.tab.options);
app.page.receive("storage", core.update.page);
app.hotkey.on.pressed(core.action.hotkey.pressed);
app.options.receive("white-list", core.update.options);
app.popup.receive("add-whitelist", core.action.hotkey.add);
app.popup.receive("remove-whitelist", core.action.hotkey.remove);
app.popup.receive("support", function () {app.tab.open(app.homepage())});
app.popup.receive("donation", function () {app.tab.open(app.homepage() + "?reason=support")});

app.on.startup(core.start);
app.on.installed(core.install);
app.on.storage(core.action.storage);

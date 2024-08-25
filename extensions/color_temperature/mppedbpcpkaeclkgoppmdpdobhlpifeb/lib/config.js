var config = {};

config.welcome = {
  set lastupdate (val) {app.storage.write("lastupdate", val)},
  get lastupdate () {return app.storage.read("lastupdate") !== undefined ? app.storage.read("lastupdate") : 0}
};

config.whitelist = {
  set array (val) {app.storage.write("whitelist", JSON.stringify(val))},
  get array () {return app.storage.read("whitelist") !== undefined ? JSON.parse(app.storage.read("whitelist")) : []}
};

config.hotkey = {
  set add (val) {app.storage.write("hotkey-add", val)},
  set mode (val) {app.storage.write("hotkey-mode", val)},
  set remove (val) {app.storage.write("hotkey-remove", val)},
  get add () {return app.storage.read("hotkey-add") !== undefined ? app.storage.read("hotkey-add") : true},
  get mode () {return app.storage.read("hotkey-mode") !== undefined ? app.storage.read("hotkey-mode") : true},
  get remove () {return app.storage.read("hotkey-remove") !== undefined ? app.storage.read("hotkey-remove") : true}
};

config.dimmer = {
  set mode (val) {app.storage.write("dimmerMode", val)},
  get mode () {return app.storage.read("dimmerMode") !== undefined ? app.storage.read("dimmerMode").toUpperCase() : "ON"},
  //
  get R () {return app.storage.read("dimmerR") !== undefined ? parseInt(app.storage.read("dimmerR")) : 255},
  set R (val) {
    if (!val || isNaN(val)) val = 0;
    val = parseInt(val);
    if (val < 0) val = 0;
    if (val > 255) val = 255;
    app.storage.write("dimmerR", val);
  },
  get G () {return app.storage.read("dimmerG") !== undefined ? parseInt(app.storage.read("dimmerG")) : 147},
  set G (val) {
    if (!val || isNaN(val)) val = 0;
    val = parseInt(val);
    if (val < 0) val = 0;
    if (val > 255) val = 255;
    app.storage.write("dimmerG", val);
  },
  get B () {return app.storage.read("dimmerB") !== undefined ? parseInt(app.storage.read("dimmerB")) : 41},
  set B (val) {
    if (!val || isNaN(val)) val = 0;
    val = parseInt(val);
    if (val < 0) val = 0;
    if (val > 255) val = 255;
    app.storage.write("dimmerB", val);
  },
  get A () {return app.storage.read("dimmerA") !== undefined ? parseInt(app.storage.read("dimmerA")) : 30},
  set A (val) {
    if (!val || isNaN(val)) val = 0;
    val = parseInt(val);
    if (val < 0) val = 0;
    if (val > 100) val = 100;
    app.storage.write("dimmerA", val);
  }
};

config.get = function (name) {
  return name.split('.').reduce(function (p, c) {return p[c]}, config);
};

config.set = function (name, value) {
  function set(name, value, scope) {
    name = name.split('.');
    if (name.length > 1) {
      set.call((scope || this)[name.shift()], name.join('.'), value);
    } else {
      this[name[0]] = value;
    }
  }
  /*  */
  set(name, value, config);
};

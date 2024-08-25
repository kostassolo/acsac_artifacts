/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ({

/***/ 3:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


function notifyContentScript(config) {
  console.log('notifying contentscript');
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { message: 'applyConfigInContentScript', config: config },
      function() {}
    );
  });
}

// default user store
var DEFAULT_CONFIG = {
  enabled: 1,
  font: 'opendyslexic',
  rulerEnabled: 1,
  rulerWidth: '26'
};

var subscribers = [];
var store = {
  /**
   * Interpolate form data with what's in the store, in case values are missing from the form
   * then save.
   */
  update: function(newData, cb) {
    chrome.storage.sync.get('config', function(store) {
      var updated = Object.assign(store.config, newData);
      chrome.storage.sync.set({ config: updated }, function() {
        console.log('Saved config', updated);
        // notify subscribers
        subscribers.forEach(function(cb) {
          cb(updated);
        });
        return cb ? cb(updated) : true;
      });
    });
  },

  get: function(key, cb) {
    chrome.storage.sync.get('config', function(store) {
      var config = store.config || DEFAULT_CONFIG; // fallback to default store

      // don't do this
      if (!key) {
        return cb(config);
      }
      return cb ? cb(config[key]) : true;
    });
  },

  // subscribe to changes in store
  subscribe: function(cb) {
    subscribers.push(cb);
    cb(store);
  }
};

/**
 * Installed
 */

// save default store if not exists
chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.get('config', function(data) {
    if (!data.config) {
      chrome.storage.sync.set({ config: DEFAULT_CONFIG }, function() {
        console.log('Default config saved', DEFAULT_CONFIG);
      });
    }
  });
});

/**
 * Runtime
 */

// listen for messages
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.message === 'updateConfig') {
    store.update(request.data);
  } else if (request.message === 'init') {
    store.get(null, sendResponse);
    return true; // otherwise sendResponse won't be called
  }
});

// 1) apply config on navigation
// NOTE: seems to run many times on one nav
chrome.webNavigation.onCommitted.addListener(function() {
  // Run as soon as a navigation has been committed
  // i.e. before document has loaded

  console.log('onCommitted');
  store.get(null, notifyContentScript);
});

// 2) apply config on tab switch
chrome.tabs.onActivated.addListener(function() {
  console.log('onActivated');
  store.get(null, notifyContentScript);
});

// 3) apply config on store change for current tab
store.subscribe(notifyContentScript);


/***/ })

/******/ });
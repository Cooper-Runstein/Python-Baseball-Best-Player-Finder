const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  window = new BrowserWindow({ width: 800, height: 600 });
  window.loadFile("index.html");
};

const runApp = () => {
  app.on("ready", createWindow);
};

module.exports = runApp;

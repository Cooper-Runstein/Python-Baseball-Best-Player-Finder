const ipc = require("electron").ipcRenderer;
let { PythonShell } = require("python-shell");

const render = ()=>{
    console.log('we made it to this page')
    PythonShell.run("../../python/main.py", null, (err, results) => {
        if (err) {
          throw err;
        }
        console.log("main.py ran");
        const hello = document.getElementById("hello");
        hello.innerText = results;
      });
}

module.exports = render
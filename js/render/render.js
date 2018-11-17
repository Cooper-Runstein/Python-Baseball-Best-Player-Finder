const ipc = require("electron").ipcRenderer;

let { PythonShell } = require("python-shell");

const render = () => {
  console.log("HELLO");
  const runPython = team => {
    let options = {
      args: [team]
    };
    PythonShell.run("python/main.py", options, (err, results) => {
      if (err) {
        throw err;
      }
      console.log("main.py ran");
      const hello = document.getElementById("hello");
      hello.innerText = results;
    });
  };

  document.getElementById("button").addEventListener("click", () => {
    const team = document.getElementById("input").value;
    console.log(team);
    runPython(team);
  });

  runPython("bos");
};

module.exports = render;

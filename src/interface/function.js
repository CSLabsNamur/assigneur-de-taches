function generateOutput() {
  const path = require("path");
  const exec = require("child_process").execFile;
  global.appRoot = path.resolve(__dirname);

  console.log(
    String.raw`D:\Dossier\Document\GitHub\assigneur-de-taches\src\electron-interface\Start.bat`
  );
  let pathBat = `${appRoot.split("\\interface")[0]}\\Start.bat`;
  console.log(pathBat);
  exec(pathBat, (err, stdout, stderr) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(stdout);
  });
}

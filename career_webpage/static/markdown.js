let stored_md = "";

async function update_md(value) {
    stored_md = value

    const converter = new showdown.Converter();
    const html = converter.makeHtml(value);

    const target = document.getElementById('rendered_md')

    target.innerHTML = html
}

function download_md(filename) {
    download(filename, stored_md)
}

function download(filename, text) {
  const element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function startSpinner() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function stopSpinner() {
    document.getElementById('loadingOverlay').style.display = 'none';

}

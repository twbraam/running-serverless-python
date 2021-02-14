async function getSignatures(apiUrl, extension) {
  if (!apiUrl) {
    throw 'Please provide an API URL';
  }
  if (!extension) {
    throw 'Please provide an extension';
  }
  const response = await fetch(`${apiUrl}sign/${extension}`);
  if (response.ok) {
    return response.json();
  } else {
    const error = await response.text();
    throw error;
  }
};
function postFormData(url, formData, progress) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    const sendError = (e, label) => {
      console.error(e);
      reject(label);
    };
    request.open('POST', url);
    request.upload.addEventListener('error', e =>
      sendError(e, 'upload error')
    );
    request.upload.addEventListener('timeout', e =>
      sendError(e, 'upload timeout')
    );
    request.upload.addEventListener('progress', progress);
    request.addEventListener('load', () => {
      if (request.status >= 200 && request.status < 400) {
        resolve();
      } else {
        reject(request.responseText);
      }
    });
    request.addEventListener('error', e =>
      sendError(e, 'server error')
    );
    request.addEventListener('abort', e =>
      sendError(e, 'server aborted request')
    );
    request.send(formData);
  });
};
function parseXML(xmlString, textQueryElement) {
  const parser = new DOMParser(),
    doc = parser.parseFromString(xmlString, 'application/xml'),
    element = textQueryElement && doc.querySelector(textQueryElement);
  if (!textQueryElement) {
    return doc;
  }
  return element && element.textContent;
};
function uploadBlob(uploadPolicy, fileBlob, progress) {
  const formData = new window.FormData();
  Object.keys(uploadPolicy.fields).forEach((key) =>
    formData.append(key, uploadPolicy.fields[key])
  );
  formData.append('file', fileBlob);
  return postFormData(uploadPolicy.url, formData, progress)
    .catch(e => {
      if (parseXML(e, 'Code') === 'EntityTooLarge') {
        throw `File ${fileBlob.name} is too big to upload.`;
      };
      throw 'server error';
    });
};
function promiseTimeout(timeout) {
  return new Promise(resolve => {
    setTimeout(resolve, timeout);
  });
};
async function pollForResult(url, timeout, times) {
  if (times <= 0) {
    throw 'no retries left';
  }
  await promiseTimeout(timeout);
  try {
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Range': 'bytes=0-10'
      }
    });
    if (!response.ok) {
      console.log('file not ready, retrying');
      return pollForResult(url, timeout, times - 1);
    }
    return 'OK';
  } catch (e) {
    console.error('network error');
    console.error(e);
    return pollForResult(url, timeout, times - 1);
  }
};
function showStep(label) {
  const sections = Array.from(document.querySelectorAll('[step]'));
  sections.forEach(section => {
    if (section.getAttribute('step') === label) {
      section.style.display = '';
    } else {
      section.style.display = 'none';
    }
  });
};
function progressNotifier(progressEvent) {
  const progressElement = document.getElementById('progressbar');
  const total = progressEvent.total;
  const current = progressEvent.loaded;
  if (current && total) {
    progressElement.setAttribute('max', total);
    progressElement.setAttribute('value', current);
  }
};
async function startUpload(evt) {
  const picker = evt.target;
  const file = picker.files && picker.files[0];
  const apiUrl = document.getElementById('apiurl').value;

  if (file && file.name) {
    picker.value = '';
    try {
      const extension = file.name.replace(/.+\./g, '');
      if (!extension) {
        throw `${file.name} has no extension`;
      }
      showStep('uploading');
      const signatures = await getSignatures(apiUrl, extension);
      console.log('got signatures', signatures);
      await uploadBlob(signatures.upload, file, progressNotifier);
      showStep('converting');
      await pollForResult(signatures.download, 3000, 20);
      const downloadLink = document.getElementById('resultlink');
      downloadLink.setAttribute('href', signatures.download);
      showStep('result');
    } catch (e) {
      console.error(e);
      const displayError = e.message || JSON.stringify(e);
      document.getElementById('errortext').innerHTML = displayError;
      showStep('error');
    }
  }
};
function initPage() {
  const picker = document.getElementById('picker');
  showStep('initial');
  picker.addEventListener('change', startUpload);
};
window.addEventListener('DOMContentLoaded', initPage);

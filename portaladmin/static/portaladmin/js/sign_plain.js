function start_signing(){
    const ASYNC_FALSE = false;

    function getstarturl() {
        var xhr = new XMLHttpRequest();
        var url = location.origin + '/sigproxyapi/getstarturl/1/'  // id hard-coded for test
            // + document.querySelector(".field-id div div").textContent + '/'
        xhr.open("GET", url, ASYNC_FALSE);
        try {
            xhr.send(null);
            return xhr.responseText;
        } catch (e) {
            alert('Cannot get start-url for signing process. ' + e.toString() + 'URL: ' + url)
        }
    }

    function exec_starturl() {
        var xhr = new XMLHttpRequest();
        var url = getstarturl()
        xhr.open("GET", url, ASYNC_FALSE);
        try {
            xhr.send(null);
        } catch (e) {
            alert('Cannot start signing process. ' + e.toString() + 'URL: ' + url)
        }
    }

    if (document.readyState === "complete")
        exec_starturl()
};

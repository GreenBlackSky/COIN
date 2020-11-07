async function submit_numbers() {

    let entry = {
        num1: document.getElementById("num1").value,
        num2: document.getElementById("num2").value
    };

    let response = await fetch(
        `${window.origin}/`,
        {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({"content-type": "application/json"})
        }
    );

    if(response.ok) {
        let responseJSON = await response.json();
        alert('Result is: ' + responseJSON["result"]);
    } else {
        alert('HTTP error ' + response.status);
    }

};

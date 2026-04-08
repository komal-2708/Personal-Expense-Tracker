document.addEventListener("DOMContentLoaded", function () {
    const remainingMoney = document.getElementById("remaining-money");

    if (remainingMoney) {
        const value = remainingMoney.innerText.replace("₹", "").trim();
        const numberValue = parseFloat(value);

        if (numberValue < 0) {
            remainingMoney.style.color = "red";
        } else {
            remainingMoney.style.color = "green";
        }
    }
});
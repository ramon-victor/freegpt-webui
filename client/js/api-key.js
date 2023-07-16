const showApiKeyButton = document.getElementById("show-api-key-button");  
const apiKeyInput = document.getElementById("API-key");  
const apiKeyOkButton = document.getElementById("api-key-ok-button");  
  
showApiKeyButton.addEventListener("click", () => {  
  showApiKeyButton.classList.add("hidden");  
  
  apiKeyInput.classList.remove("hidden");  
  apiKeyOkButton.classList.remove("hidden");  
});  
  
apiKeyOkButton.addEventListener("click", () => {  
  localStorage.setItem("API-key", apiKeyInput.value);  
  
  apiKeyInput.classList.add("hidden");  
  apiKeyOkButton.classList.add("hidden");  
  
  showApiKeyButton.classList.remove("hidden");  
});  
  
window.addEventListener("DOMContentLoaded", () => {  
  const apiKey = localStorage.getItem("API-key");  
  if (apiKey) {  
    apiKeyInput.value = apiKey;  
  }  
});  

(function () {  
  function getApiKeyFromLocalStorage() {  
    return localStorage.getItem("API-key");  
  }  
  window.getApiKeyFromLocalStorage = getApiKeyFromLocalStorage;  
})();  

function toggleSidebar(event) {
    const sidebar = document.querySelector(".sidebar");

    if (sidebar.classList.contains("shown")) {
        hideSidebar(sidebar, event.target);
    } else {
        showSidebar(sidebar, event.target);
    }

    window.scrollTo(0, 0);
}

function showSidebar(sidebar, target) {
    sidebar.classList.add("shown");
    target.classList.add("rotated");
    document.body.style.overflow = "hidden";
}

function hideSidebar(sidebar, target) {
    sidebar.classList.remove("shown");
    target.classList.remove("rotated");
    document.body.style.overflow = "auto";
}

document.querySelector(".menu-button").addEventListener("click", toggleSidebar);
